from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.documents import Document

from document_loader import load_and_split_pdf

from config import (
    PDF_PATH,
    EMBEDDING_MODEL,
    QDRANT_URL,
    QDRANT_COLLECTION_NAME,
    TOP_K,
    RECREATE_COLLECTION)

def get_embeddings() -> OpenAIEmbeddings:
    """임베딩 모델을 생성한다."""
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)

def get_qdrant_client() -> QdrantClient:
    """Qdrant 클라이언트를 생성하고 연결 상태를 확인한다."""
    client = QdrantClient(url=QDRANT_URL, timeout=10)

    try:
        collections = client.get_collections().collections
        print("Qdrant 연결 성공")
        print("현재 collection 목록:")

        if not collections:
            print("- 현재 생성된 collection이 없습니다.")
        else:
            for collection in collections:
                print("-", collection.name)

    except Exception as e:
        raise RuntimeError(
            "Qdrant Server에 연결할 수 없습니다. "
            "Docker Desktop이 실행 중인지, qdrant-rag 컨테이너가 실행 중인지 확인하세요. "
            "Web UI: http://localhost:6333/dashboard"
        ) 

    return client

def collection_exists(client: QdrantClient, collection_name: str) -> bool:
    """Qdrant collection 존재 여부를 확인한다."""
    try:
        return client.collection_exists(collection_name)
    except AttributeError:
        names = [c.name for c in client.get_collections().collections]
        return collection_name in names
    
def build_vectorstore(
    client: QdrantClient,
    embeddings: OpenAIEmbeddings,
    documents: list[Document] | None = None,
) -> QdrantVectorStore:
    """
    Qdrant 벡터스토어를 준비한다.

    RECREATE_COLLECTION = True:
        기존 collection이 있으면 삭제 후 새로 생성하고 문서를 다시 임베딩한다.

    RECREATE_COLLECTION = False:
        기존 collection을 재사용한다. 새 임베딩을 생성하지 않는다.
    """

    exists = collection_exists(client, QDRANT_COLLECTION_NAME)
    print(f"collection exists before run: {exists}")

    if RECREATE_COLLECTION:
        if documents is None or len(documents) == 0:
            raise ValueError("RECREATE_COLLECTION=True일 때는 documents가 필요합니다.")

        print("collection을 새로 생성합니다. 기존 collection이 있으면 삭제 후 재생성합니다.")

        vector_store = QdrantVectorStore.from_documents(
            documents=documents,
            embedding=embeddings,
            url=QDRANT_URL,
            collection_name=QDRANT_COLLECTION_NAME,
            force_recreate=True,
        )

    else:
        if not exists:
            raise ValueError(
                f"'{QDRANT_COLLECTION_NAME}' collection이 아직 없습니다. "
                "처음 실행할 때는 RECREATE_COLLECTION = True로 설정하세요."
            )

        print("기존 collection을 재사용합니다. 새 임베딩을 생성하지 않습니다.")

        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            collection_name=QDRANT_COLLECTION_NAME,
            url=QDRANT_URL,
        )

    print("vector_store 준비 완료")
    return vector_store


def search_documents(
        vectorstore: QdrantVectorStore, 
        query: str, 
        k: int = TOP_K
        ) -> list[Document]:
    """질문과 유사한 문서를 검색한다."""
    return vectorstore.similarity_search(query, k=k)

if __name__ == "__main__":
    print("1. Qdrant 클라이언트 생성 중...")
    client = get_qdrant_client()

    print("2. 임베딩 모델 생성 중...")
    embeddings = get_embeddings()

    documents = None

    if RECREATE_COLLECTION:
        print("3. PDF 로딩 및 청크 분할 중...")
        documents = load_and_split_pdf(PDF_PATH)
        print(f"   생성된 청크 수: {len(documents)}")
    else:
        print("3. 기존 collection 재사용 모드입니다. PDF 로딩을 생략합니다.")

    print("4. Qdrant 벡터스토어 생성 중...")
    vectorstore = build_vectorstore(
        client=client,
        embeddings=embeddings,
        documents=documents,
    )

    print("5. 벡터스토어에서 유사한 문서 검색 중...")
    query = "민원인이 반복 전화를 하면 어떻게 해야 하나요?"

    results = search_documents(vectorstore, query)

    print(f"   검색된 문서 수: {len(results)}")

    for i, doc in enumerate(results, start=1):
        print(
            f"   [{i}] "
            f"{doc.metadata.get('source')} - "
            f"페이지 {doc.metadata.get('page')}, "
            f"섹션: {doc.metadata.get('section')}, "
            f"토픽: {doc.metadata.get('topic')}"
        )