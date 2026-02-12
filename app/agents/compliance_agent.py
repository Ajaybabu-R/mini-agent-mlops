from app.tools.dummy_api import compliance_check


def compliance_agent(state):

    trace = state.get("trace")
    span = None

    if trace:
        span = trace.span(name="compliance_agent")

    retrieved_docs = state.get("retrieved_docs", [])

    if span:
        span.update(input={"retrieved_docs": retrieved_docs})

    compliance_result = compliance_check(retrieved_docs)

    if span:
        span.update(output={"compliance_result": compliance_result})
        span.end()

    state["compliance_result"] = compliance_result

    return state
