def preview_text(text: str, max_len: int = 200) -> str:
    if text is None:
        return ""

    text = str(text).replace("\n", " ")
    return text[:max_len] + "..." if len(text) > max_len else text


def print_stream_outputs(app, initial_state: dict) -> None:
    print("=== stream() 실행 결과 ===")

    for event in app.stream(initial_state, stream_mode="updates"):
        node_name = list(event.keys())[0]
        node_output = event[node_name]

        print(f"\n[{node_name}]")

        if node_name == "classify_question":
            print("case_type:", node_output.get("case_type"))
            print("rewritten_query:", preview_text(node_output.get("rewritten_query")))

        elif node_name == "retrieve_manual":
            documents = node_output.get("documents", [])
            context = node_output.get("context", "")

            print("검색 문서 수:", len(documents))
            print("context 길이:", len(context))

        elif node_name == "organize_evidence":
            print("evidence:", preview_text(node_output.get("evidence")))

        elif node_name == "generate_answer":
            print("answer:", preview_text(node_output.get("answer")))

        elif node_name == "validate_answer":
            print("validation:", preview_text(node_output.get("validation")))