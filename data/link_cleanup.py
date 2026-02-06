import re
from pathlib import Path

# Folder containing markdown files
MD_FOLDER = Path("md_articles/tempt")

# Regex to match markdown links: [text](url)
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\([^)]+\)")

def remove_links_from_markdown(md_text: str) -> str:
    return LINK_PATTERN.sub(r"\1", md_text)

def main():
    for md_file in MD_FOLDER.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        cleaned = remove_links_from_markdown(content)
        md_file.write_text(cleaned, encoding="utf-8")
        print(f"Processed: {md_file.name}")

if __name__ == "__main__":
    main()
