from typing_extensions import TypedDict, NotRequired
from langchain_core.documents import Document


class RAGState(TypedDict):
    question: str
    case_type: NotRequired[str]
    rewritten_query: NotRequired[str]
    documents: NotRequired[list[Document]]
    context: NotRequired[str]
    evidence: NotRequired[str]
    answer: NotRequired[str]
    validation: NotRequired[str]
