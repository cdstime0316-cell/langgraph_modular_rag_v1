from pathlib import Path
import os

from pathlib import Path

# 현재 폴더의 상위 폴더
BASE_DIR = Path.cwd().resolve().parent
DATA_DIR = BASE_DIR / Path("data")
PDF_PATH = DATA_DIR / "공직자_민원응대_핵심_매뉴얼.pdf"

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

QDRANT_URL = "http://localhost:6333"
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "civil_service_manual")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "700"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
TOP_K = int(os.getenv("TOP_K", "4"))

# True: collection을 삭제 후 새로 생성한다.
# False: 이미 저장된 collection을 재사용한다.
RECREATE_COLLECTION = True
