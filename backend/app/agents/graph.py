from langgraph.graph import StateGraph, END
from typing import TypedDict
from backend.app.services.groq_services import call_llm

from backend.app.agents.tools import (
    log_interaction_tool,
    edit_interaction_tool,
    summarize_tool,
    extract_entities_tool,
    followup_tool
)


class AgentState(TypedDict):
    query: str
    intent: str
    result: dict


def detect_intent(state: AgentState):
    query = state["query"]
    q = query.lower()

    # 🔥 HARD RULE FIRST (VERY IMPORTANT)
    if any(word in q for word in ["met", "discussed", "visited", "interaction"]):
        intent = "create"

    elif any(word in q for word in ["sorry", "actually", "change", "update", "correct", "was"]):
        intent = "edit"

    elif "summary" in q:
        intent = "summarize"

    elif "extract" in q:
        intent = "extract"

    else:
        # fallback to LLM (optional)
        try:
            prompt = f"""
Classify into one word:

create, edit, summarize, extract, followup

Input: {query}
"""
            raw_intent = call_llm(prompt)
            temp = raw_intent.strip().lower()

            if "edit" in temp:
                intent = "edit"
            elif "create" in temp:
                intent = "create"
            elif "summarize" in temp:
                intent = "summarize"
            elif "extract" in temp:
                intent = "extract"
            else:
                intent = "followup"

        except:
            intent = "followup"

    print("FINAL INTENT:", intent)

    return {"intent": intent}

def tool_node(state: AgentState):
    query = state["query"]
    intent = state["intent"]

    print("TOOL NODE INTENT:", intent)

    if intent == "edit":
        result = edit_interaction_tool(1, query)

    elif intent == "create":
        result = log_interaction_tool(query)

    elif intent == "summarize":
        result = summarize_tool(query)

    elif intent == "extract":
        result = extract_entities_tool(query)

    else:
        result = followup_tool(query)

    return {"result": result}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent_node", detect_intent)
    graph.add_node("tool_node", tool_node)

    graph.set_entry_point("intent_node")

    graph.add_edge("intent_node", "tool_node")
    graph.add_edge("tool_node", END)

    return graph.compile()


agent = build_graph()


def run_agent(query: str):
    return agent.invoke({"query": query})