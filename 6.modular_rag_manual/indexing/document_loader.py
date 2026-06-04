# indexing/document_loader.py
# PS E:\langgraph_modular_rag\6.modular_rag_manual> python indexing/document_loader.py

import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def clean_text(text: str) -> str:
    """PDF에서 추출된 텍스트를 간단히 정제한다."""
    text = text.replace("\x00", " ")
    text = text.replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_pdf_pages(pdf_path: Path) -> list[Document]:
    """PDF를 페이지 단위 Document 리스트로 로드한다."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()

    page_docs = []

    for doc in docs:
        text = clean_text(doc.page_content or "")

        if not text:
            continue

        page_docs.append(
            Document(
                page_content=text,
                metadata={
                    **doc.metadata,
                    "source": pdf_path.name,
                    "page": doc.metadata.get("page", 0) + 1,
                },
            )
        )

    return page_docs


if __name__ == "__main__":
    from common.config import PDF_PATH

    pages = load_pdf_pages(PDF_PATH)

    print("추출된 페이지 수:", len(pages))

    if pages:
        print("\n[첫 번째 페이지 metadata]")
        print(pages[0].metadata)

        print("\n[첫 번째 페이지 preview]")
        print(pages[0].page_content[:500])