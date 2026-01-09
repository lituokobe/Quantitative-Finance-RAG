from pathlib import Path

current_file = Path(__file__).resolve()
project_dir = current_file.parent.parent

LOG_PATH = project_dir / "logs"
ENV_PATH = project_dir / ".env"
MD_PATH = project_dir / "data/md_articles"
QWEN3_EMBEDDING_PATH = project_dir /"models/Qwen3-Embedding-0.6B"
MILVUS_URI = "http://127.0.0.1/19530"
