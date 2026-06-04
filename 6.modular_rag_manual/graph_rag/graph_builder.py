from langgraph.graph import StateGraph, START, END

from graph_state import ModularRAGState
from graph_nodes import (
    classify_question_node,
    retrieve_manual_node,
    organize_evidence_node,
    generate_answer_node,
    validate_answer_node,
)


def build_graph():
    graph = StateGraph(ModularRAGState)

    graph.add_node("classify_question", classify_question_node)
    graph.add_node("retrieve_manual", retrieve_manual_node)
    graph.add_node("organize_evidence", organize_evidence_node)
    graph.add_node("generate_answer", generate_answer_node)
    graph.add_node("validate_answer", validate_answer_node)

    graph.add_edge(START, "classify_question")
    graph.add_edge("classify_question", "retrieve_manual")
    graph.add_edge("retrieve_manual", "organize_evidence")
    graph.add_edge("organize_evidence", "generate_answer")
    graph.add_edge("generate_answer", "validate_answer")
    graph.add_edge("validate_answer", END)

    return graph.compile()




if __name__ == "__main__":
    
    app = build_graph()

    question = "대면 민원 중 폭행이 발생하면 어떻게 해야 하나요?"
    print(f"질문: {question}\n")
    result = app.invoke({
        "question": question
    })
    print("\n[답변 생성중입니다. 잠시만 기다려주세요...]\n")
    print("──────────────────────────────────────────────\n")
    print("[질문 유형]")
    print(result["case_type"])

    print("\n[검색 질의]")
    print(result["rewritten_query"])

    print("\n[근거 정리]")
    print(result["evidence"])

    print("\n[답변]")
    print(result["answer"])

    print("\n[검증]")
    print(result["validation"])
