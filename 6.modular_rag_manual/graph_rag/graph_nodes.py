from graph_state import ModularRAGState
from classifier import classify_question
from vectorstore import vector_store
from utils import format_docs
from chains import evidence_chain, answer_chain, validation_chain


def classify_question_node(state: ModularRAGState) -> dict:
    result = classify_question(state["question"])

    return {
        "case_type": result["case_type"],
        "rewritten_query": result["rewritten_query"],
    }


def retrieve_manual_node(state: ModularRAGState) -> dict:
    query = state.get("rewritten_query") or state["question"]
    docs = vector_store.similarity_search(query, k=4)
    context = format_docs(docs)

    return {
        "documents": docs,
        "context": context,
    }


def organize_evidence_node(state: ModularRAGState) -> dict:
    evidence = evidence_chain.invoke({
        "question": state["question"],
        "context": state["context"],
    })

    return {
        "evidence": evidence,
    }


def generate_answer_node(state: ModularRAGState) -> dict:
    answer = answer_chain.invoke({
        "question": state["question"],
        "evidence": state["evidence"],
    })

    return {
        "answer": answer,
    }


def validate_answer_node(state: ModularRAGState) -> dict:
    validation = validation_chain.invoke({
        "question": state["question"],
        "context": state["context"],
        "answer": state["answer"],
    })

    return {
        "validation": validation,
    }