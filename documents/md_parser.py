import re
from typing import Any
from dataclasses import dataclass
from pathlib import Path
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker

from models.models import qwen3_embedding_model


# ============================================================
# Internal block representation
# ============================================================
@dataclass
class Block:
    kind: str          # paragraph | table | math | list
    text: str
    metadata: dict[str, Any]


# ============================================================
# Utilities: robust detectors
# ============================================================

def contains_math(text: str) -> bool:
    """Detect LaTeX-style math."""
    if re.search(r"\$\$[\s\S]+?\$\$", text):
        return True
    if re.search(r"(?<!\\)\$.*?(?<!\\)\$", text, flags=re.DOTALL):
        return True
    latex_commands = [
        r"\\frac\{", r"\\sum", r"\\sqrt", r"\\int", r"\\lim",
        r"\\begin\{equation", r"\\begin\{align", r"\\cdot"
    ]
    return any(re.search(cmd, text) for cmd in latex_commands)


def looks_like_table(text: str) -> bool:
    """
    Detect Markdown tables even when mixed with headings or prose.

    A table is detected if the block contains >= 2 consecutive lines
    that each contain at least one '|' character.
    """
    lines = [l for l in text.splitlines() if l.strip()]
    pipe_run = 0

    for l in lines:
        if "|" in l:
            pipe_run += 1
            if pipe_run >= 2:
                return True
        else:
            pipe_run = 0

    return False


def is_list_block(text: str) -> bool:
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return False
    for l in lines:
        s = l.strip()
        if s.startswith(("-", "*")):
            continue
        head = s.split(".", 1)[0]
        if not head.isdigit():
            return False
    return True


# ============================================================
# Finance Markdown Parser (no Unstructured)
# ============================================================
class FinanceMarkdownParser:
    """
    Production-grade markdown parser for finance RAG.
    """

    def __init__(
        self,
        max_chars_per_chunk: int = 1400,
        semantic_refine_threshold: int = 1800,
        semantic_chunker: SemanticChunker | None = None, # semantic chunking is good for long narratives, but not friendly to structured documents with maths & tables
    ):
        self.max_chars_per_chunk = max_chars_per_chunk
        self.semantic_refine_threshold = semantic_refine_threshold
        self.semantic_chunker = semantic_chunker

    # ============================================================
    # STEP 1: Load raw markdown
    # ============================================================
    def _load_raw_markdown(self, md_file: str) -> str:
        with open(md_file, "r", encoding="utf-8") as f:
            return f.read()

    # ============================================================
    # STEP 2: Build section-level documents
    # ============================================================
    def _build_sections(self, raw_text: str, source: str, filename: str) -> list[Document]:
        lines = raw_text.splitlines()

        sections: list[Document] = []
        current_lines: list[str] = []
        hierarchy: dict[int, str] = {}
        current_meta: dict[str, Any] = {}

        heading_pattern = re.compile(r"^(#{1,6})\s+(.*)$")

        def flush_section():
            nonlocal current_lines, current_meta
            if not current_lines:
                return
            content = "\n".join(current_lines).strip()
            if content:
                sections.append(Document(page_content=content, metadata=dict(current_meta)))
            current_lines = []
            current_meta = {}

        for line in lines:
            m = heading_pattern.match(line)
            if m:
                flush_section()
                hashes, title_text = m.groups()
                level = len(hashes)
                hierarchy[level] = title_text.strip()
                for deeper in range(level + 1, 7):
                    hierarchy.pop(deeper, None)

                breadcrumb = " > ".join(
                    hierarchy[i] for i in sorted(hierarchy.keys()) if hierarchy.get(i)
                )

                current_meta = {
                    "category": "section",
                    "title": title_text.strip(),
                    "breadcrumb": breadcrumb,
                    "section_level": level,
                    "source": source,
                    "filename": filename,
                }
                current_lines = [title_text.strip()]
            else:
                if not current_meta:
                    current_meta = {
                        "category": "section",
                        "title": "",
                        "breadcrumb": "",
                        "section_level": 0,
                        "source": source,
                        "filename": filename,
                    }
                current_lines.append(line)

        flush_section()
        return sections

    # ============================================================
    # STEP 3: Segment into atomic blocks
    # ============================================================
    def _segment_into_blocks(self, doc: Document) -> list[Block]:
        content = doc.page_content
        lines = content.splitlines()

        blocks: list[Block] = []
        buf: list[str] = []

        def flush():
            if not buf:
                return
            text = "\n".join(buf).strip()
            kind = self._classify_block(text)
            blocks.append(
                Block(
                    kind=kind,
                    text=text,
                    metadata={
                        **doc.metadata,
                        "block_type": kind,
                        "contains_math": contains_math(text),
                        "contains_table": looks_like_table(text),
                    },
                )
            )
            buf.clear()

        for line in lines:
            if not line.strip():
                flush()
                continue
            buf.append(line)

        flush()
        return blocks

    def _classify_block(self, text: str) -> str:
        if looks_like_table(text):
            return "table"
        if contains_math(text):
            return "math"
        if is_list_block(text):
            return "list"
        return "paragraph"

    # ============================================================
    # STEP 4: Pack blocks
    # ============================================================
    def _pack_blocks(self, blocks: list[Block]) -> list[Document]:
        chunks: list[Document] = []
        buf: list[str] = []
        buf_len = 0
        buf_meta: dict[str, Any] = {}
        buf_contains_math = False
        buf_contains_table = False

        def flush():
            nonlocal buf, buf_len, buf_meta, buf_contains_math, buf_contains_table
            if not buf:
                return
            combined = "\n\n".join(buf).strip()
            meta = dict(buf_meta)
            if buf_contains_math:
                meta["contains_math"] = True
            if buf_contains_table:
                meta["contains_table"] = True
            chunks.append(Document(page_content=combined, metadata=meta))
            buf = []
            buf_len = 0
            buf_meta = {}
            buf_contains_math = False
            buf_contains_table = False

        for blk in blocks:
            blen = len(blk.text)

            if blen > self.max_chars_per_chunk:
                flush()
                chunks.append(Document(page_content=blk.text, metadata=dict(blk.metadata)))
                continue

            if buf_len + blen + 2 > self.max_chars_per_chunk:
                flush()

            if not buf:
                buf_meta = dict(blk.metadata)

            buf.append(blk.text)
            buf_len += blen + 2

            if blk.metadata.get("contains_math"):
                buf_contains_math = True
            if blk.metadata.get("contains_table"):
                buf_contains_table = True

        flush()
        return chunks

    # ============================================================
    # STEP 5: Optional semantic refinement
    # ============================================================
    def _semantic_refine(self, docs: list[Document]) -> list[Document]:
        if not self.semantic_chunker:
            return docs

        refined: list[Document] = []
        for d in docs:
            text = d.page_content

            has_math = d.metadata.get("contains_math") or contains_math(text)
            has_table = d.metadata.get("contains_table") or looks_like_table(text)

            if has_math or has_table:
                refined.append(d)
                continue

            if len(text) > self.semantic_refine_threshold:
                sub_docs = self.semantic_chunker.split_documents([d])
                for sd in sub_docs:
                    sd.metadata = dict(d.metadata)
                refined.extend(sub_docs)
            else:
                refined.append(d)

        return refined

    # ============================================================
    # MAIN PIPELINE
    # ============================================================
    def parse_markdown_to_documents(self, md_file: str) -> list[Document]:
        raw_text = self._load_raw_markdown(md_file)
        source = md_file
        filename = Path(md_file).name

        sections = self._build_sections(raw_text, source, filename)

        packed_chunks: list[Document] = []
        for doc in sections:
            blocks = self._segment_into_blocks(doc)
            packed_chunks.extend(self._pack_blocks(blocks))

        return self._semantic_refine(packed_chunks)

if __name__ == "__main__":
    # Path to your markdown file
    file_path = "../data/md_articles/MACD.md"   # change to your test file

    semantic_chunker = SemanticChunker(
        qwen3_embedding_model,
        # openai_embedding,
        breakpoint_threshold_type="percentile"
    )

    # Instantiate parser (semantic_chunker optional)
    parser = FinanceMarkdownParser(
        max_chars_per_chunk=1400,
        semantic_refine_threshold=1800,
        semantic_chunker=None, # deterministic chunker
        # semantic_chunker = semantic_chunker
    )

    # Parse into LangChain Documents
    docs = parser.parse_markdown_to_documents(file_path)

    # Pretty-print results
    print(f"\nTotal chunks produced: {len(docs)}")
    print("=" * 80)

    for idx, item in enumerate(docs):
        print(f"\n--- Chunk {idx} ---")
        print(f"Chars: {len(item.page_content)}")
        print(f"Metadata: {item.metadata}")

        # Title and breadcrumb
        print(f"Title: {item.metadata.get('title')}")
        print(f"Breadcrumb: {item.metadata.get('breadcrumb')}")

        # Flags
        print(f"Contains Math: {item.metadata.get('contains_math', False)}")
        print(f"Contains Table: {item.metadata.get('contains_table', False)}")

        # Content preview
        print("\nContent:")
        print(item.page_content)
        print("\n" + ("-" * 80))
