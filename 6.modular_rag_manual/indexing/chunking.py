# indexing/chunking.py
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from common.config import COLLECTION_NAME, EMBEDDING_MODEL
from .document_loader import load_pdf_pages

CHUNK_SIZE = 700
CHUNK_OVERLAP = 120
CHUNK_STRATEGY = "medium"


def make_medium_chunks(
    docs: list[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Document]:
    """매뉴얼형 문서에 적합한 medium chunk를 생성한다."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "STEP", "‣", "•", ". ", " "],
    )

    chunks = splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata.update(
            {
                "chunk_id": i,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "chunk_strategy": CHUNK_STRATEGY,
                "embedding_model": EMBEDDING_MODEL,
                "collection_name": COLLECTION_NAME,
            }
        )

    return chunks


if __name__ == "__main__":
    from common.config import PDF_PATH

    pages = load_pdf_pages(PDF_PATH)
    medium_chunks = make_medium_chunks(pages)

    print("페이지 수:", len(pages))
    print("medium chunk 수:", len(medium_chunks))

    if medium_chunks:
        print("\n[첫 번째 chunk metadata]")
        print(medium_chunks[0].metadata)

        print("\n[첫 번째 chunk preview]")
        print(medium_chunks[0].page_content[:500])