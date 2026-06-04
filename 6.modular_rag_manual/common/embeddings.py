# src/modular_rag_manual/common/embeddings.py

from functools import lru_cache

from langchain_openai import OpenAIEmbeddings

from config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embeddings() -> OpenAIEmbeddings:
    """프로젝트 공통 임베딩 모델을 생성한다."""

    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )


# 기존 코드와 호환되도록 전역 변수도 제공한다.
embeddings = get_embeddings()