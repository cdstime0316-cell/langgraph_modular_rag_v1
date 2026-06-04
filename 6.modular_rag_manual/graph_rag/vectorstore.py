from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from config import QDRANT_URL, COLLECTION_NAME, EMBEDDING_MODEL

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

# QdrantVectorStore를 기존 collection에서 불러온다.
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL,
)