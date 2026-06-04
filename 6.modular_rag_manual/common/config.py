# 5.modular_rag_manual/common/config.py

from pathlib import Path
import os

from dotenv import load_dotenv


# ------------------------------------------------------------
# Project Path
# ------------------------------------------------------------
# 현재 파일 위치:
# 3.modular_rag_manual/common/config.py
# parents[3] = 프로젝트 루트

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

DATA_DIR = BASE_DIR / "data"
PDF_PATH = DATA_DIR / "공직자_민원응대_핵심_매뉴얼.pdf"

# ------------------------------------------------------------
# Environment
# ------------------------------------------------------------
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)


# ------------------------------------------------------------
# Document
# ------------------------------------------------------------
PDF_PATH = Path(
    os.getenv(
        "PDF_PATH",
        str(DATA_DIR / "공직자_민원응대_핵심_매뉴얼.pdf"),
    )
)


# ------------------------------------------------------------
# Qdrant
# ------------------------------------------------------------
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_TIMEOUT = int(os.getenv("QDRANT_TIMEOUT", "10"))

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "civil_complaint_manual_medium",
)


# ------------------------------------------------------------
# Model
# ------------------------------------------------------------
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-3-small",
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gpt-4o-mini",
)


# ------------------------------------------------------------
# Retrieval
# ------------------------------------------------------------
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "4"))


# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------
def validate_common_settings() -> None:
    """공통 설정값을 점검한다."""

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY가 설정되어 있지 않습니다. "
            ".env 파일에 OPENAI_API_KEY를 추가하세요."
        )

    if not COLLECTION_NAME:
        raise ValueError("COLLECTION_NAME이 비어 있습니다.")

    if not EMBEDDING_MODEL:
        raise ValueError("EMBEDDING_MODEL이 비어 있습니다.")

    if not QDRANT_URL:
        raise ValueError("QDRANT_URL이 비어 있습니다.")