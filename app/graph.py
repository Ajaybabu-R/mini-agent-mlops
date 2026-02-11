from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.agents.retrieval_agent import retrieval_agent
from app.agents.compliance_agent import compliance_agent


class AgentState(TypedDict, total=False):
    query: str
    vector_store: object
    retrieved_docs: list
    compliance_result: str
    trace: object


def build_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("retrieval", retrieval_agent)
    workflow.add_node("compliance", compliance_agent)

    workflow.set_entry_point("retrieval")

    workflow.add_edge("retrieval", "compliance")
    workflow.add_edge("compliance", END)

    return workflow.compile()
