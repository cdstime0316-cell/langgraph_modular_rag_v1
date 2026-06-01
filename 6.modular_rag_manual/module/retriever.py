from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore

from config import TOP_K


def classify_question(question: str) -> dict:
    """질문 유형을 규칙 기반으로 간단히 분류한다."""
    q = question.lower()

    rules = [
        ("repeat_call", ["반복", "계속 전화", "같은 말", "동일"]),
        ("long_call", ["장시간", "오래", "권장시간", "20분", "15분"]),
        ("supervisor_request", ["상급자", "기관장", "부서장", "팀장"]),
        ("phone_abuse", ["전화", "욕설", "폭언", "협박", "성희롱"]),
        ("face_to_face_abuse", ["대면", "방문", "욕설", "폭언"]),
        ("violence", ["폭행", "때리", "물리", "공격"]),
        ("property_damage", ["파손", "부수", "집기", "물품"]),
        ("dangerous_object", ["위험물", "흉기", "칼", "인화물질", "불"]),
        ("online_abuse", ["온라인", "문서", "인터넷", "민원 내용"]),
        ("recovery_protection", ["보호", "휴식", "휴가", "심리", "치료"]),
        ("legal_basis", ["법", "처벌", "형량", "고소", "고발"]),
    ]

    for case_type, keywords in rules:
        if any(keyword in q for keyword in keywords):
            return {
                "case_type": case_type,
                "search_query": expand_query(question, case_type),
            }

    return {
        "case_type": "general",
        "search_query": question,
    }


def expand_query(question: str, case_type: str) -> str:
    """질문 유형별로 검색에 도움이 되는 키워드를 덧붙인다."""
    expansions = {
        "repeat_call": "정당한 사유 없는 반복 전화 동일민원 통화 종료 상담 종료",
        "long_call": "정당한 사유 없는 장시간 통화 권장시간 상담 종료",
        "supervisor_request": "상급자 기관장 통화 요구 실무자 대응 담당 팀장 대응",
        "phone_abuse": "전화응대 폭언 욕설 협박 성희롱 증거 확보 통화 종료",
        "face_to_face_abuse": "대면응대 폭언 욕설 협박 성희롱 녹화 녹음 상담 종료",
        "violence": "대면응대 폭행 비상대응팀 경찰 신고 피해공무원 분리",
        "property_damage": "집기 물품 파손 공용물건손상 경찰 신고 비상대응팀",
        "dangerous_object": "위험물 소지 흉기 인화물질 경찰 신고 119 신고 대피",
        "online_abuse": "온라인 문서민원 폭언 경고공문 부서장 보고",
        "recovery_protection": "민원담당자 회복 보호조치 휴식 휴가 심리상담 치료 지원",
        "legal_basis": "위법행위 유형별 적용 법률 형법 경범죄처벌법 공무집행방해",
    }
    return f"{question}\n검색 키워드: {expansions.get(case_type, '')}".strip()


def retrieve_manual(
    vectorstore: QdrantVectorStore,
    question: str,
    k: int = TOP_K,
    use_rewrite: bool = True,
) -> tuple[list[Document], dict]:
    """질문 분류 후 관련 문서를 검색한다."""
    info = classify_question(question)
    query = info["search_query"] if use_rewrite else question
    docs = vectorstore.similarity_search(query, k=k)
    return docs, info


def format_documents(documents: list[Document]) -> str:
    """LLM 프롬프트에 넣기 좋은 형태로 문서를 정리한다."""
    lines = []

    for i, doc in enumerate(documents, start=1):
        meta = doc.metadata
        lines.append(
            f"[근거 {i}] "
            f"page={meta.get('page')}, "
            f"section={meta.get('section')}, "
            f"topic={meta.get('topic')}\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(lines)
