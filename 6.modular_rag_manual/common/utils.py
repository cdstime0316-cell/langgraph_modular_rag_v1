# 6.modular_rag_manual/common/utils.py
from langchain_core.documents import Document


def preview_text(text: str | None, max_len: int = 200) -> str:
    """긴 텍스트를 출력용으로 짧게 줄인다."""

    if text is None:
        return ""

    text = str(text).replace("\n", " ").strip()

    if len(text) <= max_len:
        return text

    return text[:max_len] + "..."


def print_section(title: str) -> None:
    """콘솔 출력 구분선을 표시한다."""

    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_key_value(key: str, value) -> None:
    """key-value 형태로 콘솔에 출력한다."""

    print(f"{key}: {value}")


def print_document_preview(
    doc: Document,
    index: int | None = None,
    max_len: int = 300,
) -> None:
    """Document 객체의 metadata와 본문 일부를 출력한다."""

    if index is not None:
        print_section(f"[Document {index}]")
    else:
        print_section("[Document]")

    print("metadata:")
    print(doc.metadata)

    print("\npage_content preview:")
    print(preview_text(doc.page_content, max_len=max_len))


def print_documents_preview(
    docs: list[Document],
    limit: int = 3,
    max_len: int = 300,
) -> None:
    """Document 리스트 일부를 미리보기로 출력한다."""

    for i, doc in enumerate(docs[:limit], start=1):
        print_document_preview(
            doc=doc,
            index=i,
            max_len=max_len,
        )


def format_docs(docs: list[Document]) -> str:
    """검색된 Document 리스트를 RAG context 문자열로 변환한다."""

    formatted_docs = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")
        chunk_id = doc.metadata.get("chunk_id", "unknown")

        formatted_docs.append(
            f"[근거 {i}] source={source}, page={page}, chunk={chunk_id}\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(formatted_docs)