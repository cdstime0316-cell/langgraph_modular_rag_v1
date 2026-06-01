from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

from vectorstore_batch import (
    get_embeddings,
    get_qdrant_client,
    search_documents,
)

from config import (
    QDRANT_URL,
    QDRANT_COLLECTION_NAME,
    EMBEDDING_MODEL,
)

load_dotenv(override=True, dotenv_path="../../.env")

if __name__ == "__main__":
    print("1. Qdrant 클라이언트 생성 중...")
    client = get_qdrant_client()

    print("2. 임베딩 모델 생성 중...")
    embeddings = get_embeddings()

    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=QDRANT_COLLECTION_NAME,
        url=QDRANT_URL,
    )

    print("4. 벡터스토어에서 유사한 문서 검색 중...")
    query = "민원인이 반복 전화를 하면 어떻게 해야 하나요?"

    results = search_documents(vector_store, query)

    print(f"   검색된 문서 수: {len(results)}")

    for i, doc in enumerate(results, start=1):
        print(
            f"   [{i}] "
            f"{doc.metadata.get('source')} - "
            f"페이지 {doc.metadata.get('page')}, "
            f"섹션: {doc.metadata.get('section')}, "
            f"토픽: {doc.metadata.get('topic')}"
        )