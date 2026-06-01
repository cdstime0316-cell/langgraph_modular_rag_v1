from pathlib import Path
import re
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import PDF_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def clean_text(text: str) -> str:
    """PDF에서 추출된 텍스트를 검색에 적합하도록 정리한다."""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_pdf_pages(pdf_path: Path = PDF_PATH) -> list[Document]:
    """PDF를 페이지 단위 Document로 변환한다."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text() or "")
        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": pdf_path.name,
                    "page": page_number,
                    "section": infer_section(page_number, text),
                    "topic": infer_topic(text),
                },
            )
        )

    return documents

def split_documents(
    documents: list[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Document]:
    """페이지 문서를 작은 청크로 분할한다."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "STEP", "‣", "•", ". ", " "],
    )

    chunks = splitter.split_documents(documents)

    for i, doc in enumerate(chunks):
        doc.metadata["chunk_id"] = i
        doc.metadata["topic"] = infer_topic(doc.page_content)
        doc.metadata.setdefault("section", infer_section(doc.metadata.get("page", 0), doc.page_content))

    return chunks

def infer_section(page: int, text: str) -> str:
    """페이지와 키워드를 기준으로 문서 영역을 단순 분류한다."""
    if page <= 4:
        return "민원응대 관련 기본원칙"
    if page <= 7:
        return "일반적인 민원 응대요령"
    if page <= 12:
        return "특이민원 응대요령"
    if page <= 14:
        return "민원담당자 회복 및 보호조치"
    if page <= 17:
        return "질의응답"
    return "참고자료"


def infer_topic(text: str) -> str:
    """청크 본문 키워드 기준으로 주제를 단순 분류한다."""
    topic_keywords = [
        ("반복전화", ["반복 전화", "반복전화", "동일민원", "3회"]),
        ("장시간 통화", ["장시간", "권장시간", "20분", "15분"]),
        ("상급자 통화 요구", ["상급자", "기관장", "부서장", "팀장"]),
        ("전화 폭언", ["전화", "폭언", "욕설", "협박", "성희롱"]),
        ("대면 폭언", ["대면", "폭언", "욕설", "협박", "성희롱"]),
        ("폭행", ["폭행", "공무집행방해"]),
        ("물품 파손", ["파손", "집기", "공용물건"]),
        ("위험물 소지", ["위험물", "흉기", "소방서", "119"]),
        ("온라인 문서 민원", ["온라인", "문서민원", "경고공문"]),
        ("보호조치", ["휴식", "휴가", "심리상담", "치료", "피해공무원"]),
        ("법적 근거", ["형법", "경범죄", "스토킹", "적용법률"]),
    ]

    for topic, keywords in topic_keywords:
        if any(keyword in text for keyword in keywords):
            return topic
    return "일반 민원응대"

def load_and_split_pdf(pdf_path: Path = PDF_PATH) -> list[Document]:
    """PDF 로딩부터 청크 분할까지 한 번에 수행한다."""
    pages = load_pdf_pages(pdf_path)
    return split_documents(pages)

