from langgraph.graph import StateGraph, START, END
from langchain_qdrant import QdrantVectorStore

from graph_state import RAGState
from graph_nodes import create_graph_nodes


def build_basic_graph(vectorstore: QdrantVectorStore):
    """검색 → 답변 생성으로 구성된 기본 RAG 그래프."""
    nodes = create_graph_nodes(vectorstore)

    graph = StateGraph(RAGState)
    graph.add_node("retrieve_manual", nodes["retrieve_manual"])
    graph.add_node("generate_answer", nodes["generate_answer"])

    graph.add_edge(START, "retrieve_manual")
    graph.add_edge("retrieve_manual", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()


def build_modular_graph(vectorstore: QdrantVectorStore):
    """질문 분류 → 검색 → 근거 정리 → 답변 생성 → 검증 그래프."""
    nodes = create_graph_nodes(vectorstore)

    graph = StateGraph(RAGState)
    graph.add_node("classify_question", nodes["classify_question"])
    graph.add_node("retrieve_manual", nodes["retrieve_manual"])
    graph.add_node("organize_evidence", nodes["organize_evidence"])
    graph.add_node("generate_answer", nodes["generate_answer"])
    graph.add_node("validate_answer", nodes["validate_answer"])

    graph.add_edge(START, "classify_question")
    graph.add_edge("classify_question", "retrieve_manual")
    graph.add_edge("retrieve_manual", "organize_evidence")
    graph.add_edge("organize_evidence", "generate_answer")
    graph.add_edge("generate_answer", "validate_answer")
    graph.add_edge("validate_answer", END)

    return graph.compile()
