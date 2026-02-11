def retrieval_agent(state):

    trace = state.get("trace")
    span = trace.span(name="retrieval_agent")

    query = state["query"]
    vector_store = state["vector_store"]

    span.update(input={"query": query})

    results = vector_store.similarity_search(query, k=2)
    retrieved_docs = [doc.page_content for doc in results]

    span.update(output={"retrieved_docs": retrieved_docs})
    span.end()

    state["retrieved_docs"] = retrieved_docs

    return state
