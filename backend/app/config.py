from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "data" / "uploads"

CHROMA_DIR = BASE_DIR / "data" / "chroma_db"