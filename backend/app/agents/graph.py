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

    # CREATE
    if any(w in query for w in [
        "met", "meeting", "discussed", "shared",
        "distributed", "talked", "explained",
        "gave", "handed"
    ]):
        print("TOOL: CREATE")
        result = log_interaction_tool.invoke(query)

    # EDIT (🔥 FIXED)
    elif any(w in query for w in [
        "actually", "was", "change", "update", "instead",
        "samples", "sentiment", "name", "material"
    ]):
        print("TOOL: EDIT")
        result = edit_interaction_tool.invoke(query)

    elif "summarize" in query:
        print("TOOL: SUMMARIZE")
        result = summarize_tool.invoke(query)

    elif "extract" in query:
        print("TOOL: EXTRACT")
        result = extract_entities_tool.invoke(query)

    else:
        print("TOOL: FOLLOWUP")
        result = followup_tool.invoke(query)

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