from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_qdrant import QdrantVectorStore

from config import OPENAI_MODEL, TOP_K
from graph_state import RAGState
from prompts import BASIC_RAG_PROMPT, EVIDENCE_PROMPT, VALIDATION_PROMPT
from retriever import classify_question, format_documents


def create_graph_nodes(vectorstore: QdrantVectorStore) -> dict:
    """LangGraph에서 사용할 노드 함수들을 생성한다."""
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0)

    answer_chain = BASIC_RAG_PROMPT | llm | StrOutputParser()
    evidence_chain = EVIDENCE_PROMPT | llm | StrOutputParser()
    validation_chain = VALIDATION_PROMPT | llm | StrOutputParser()

    def classify_question_node(state: RAGState) -> dict:
        """사용자 질문을 간단히 분류하고 검색 질의를 확장한다."""
        result = classify_question(state["question"])
        return {
            "case_type": result["case_type"],
            "rewritten_query": result["search_query"],
        }

    def retrieve_manual_node(state: RAGState) -> dict:
        """질문 또는 확장 질의로 매뉴얼 문단을 검색한다."""
        query = state.get("rewritten_query") or state["question"]
        docs = vectorstore.similarity_search(query, k=TOP_K)
        context = format_documents(docs)
        return {
            "documents": docs,
            "context": context,
        }

    def organize_evidence_node(state: RAGState) -> dict:
        """검색 문단을 답변에 사용할 근거 형태로 정리한다."""
        evidence = evidence_chain.invoke(
            {
                "question": state["question"],
                "context": state.get("context", ""),
            }
        )
        return {"evidence": evidence}

    def generate_answer_node(state: RAGState) -> dict:
        """정리된 근거를 바탕으로 답변을 생성한다."""
        context = state.get("evidence") or state.get("context", "")
        answer = answer_chain.invoke(
            {
                "question": state["question"],
                "context": context,
            }
        )
        return {"answer": answer}

    def validate_answer_node(state: RAGState) -> dict:
        """답변이 검색 근거에 기반하는지 간단히 검토한다."""
        validation = validation_chain.invoke(
            {
                "question": state["question"],
                "context": state.get("context", ""),
                "answer": state.get("answer", ""),
            }
        )
        return {"validation": validation}

    return {
        "classify_question": classify_question_node,
        "retrieve_manual": retrieve_manual_node,
        "organize_evidence": organize_evidence_node,
        "generate_answer": generate_answer_node,
        "validate_answer": validate_answer_node,
    }
