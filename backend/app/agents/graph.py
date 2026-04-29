from langgraph.graph import StateGraph, END
from typing import TypedDict

from backend.app.agents.tools import (
    log_interaction_tool,
    edit_interaction_tool,
    summarize_tool,
    extract_entities_tool,
    followup_tool
)


class AgentState(TypedDict):
    query: str
    result: dict


def tool_node(state: AgentState):
    query = state["query"].lower()

    if "edit" in query:
        result = edit_interaction_tool(1, query)

    elif "met" in query or "log" in query:
        result = log_interaction_tool(query)

    elif "summary" in query:
        result = summarize_tool(query)

    elif "extract" in query:
        result = extract_entities_tool(query)

    else:
        result = followup_tool(query)

    return {"result": result}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("tool_node", tool_node)
    graph.set_entry_point("tool_node")
    graph.add_edge("tool_node", END)
    return graph.compile()


agent = build_graph()


def run_agent(query: str):
    return agent.invoke({"query": query})