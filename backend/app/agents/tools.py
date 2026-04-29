from langchain.tools import tool
from backend.app.services.groq_services import call_llm
from backend.app.db.session import SessionLocal
from backend.app.models.interaction import Interaction
import json


def safe_parse_json(text: str):
    try:
        return json.loads(text)
    except:
        if "{" in text and "}" in text:
            text = text[text.find("{"): text.rfind("}") + 1]
            try:
                return json.loads(text)
            except:
                return {}
        return {}


# -----------------------------
# CREATE TOOL
# -----------------------------
@tool
def log_interaction_tool(text: str):
    """Extract structured CRM data from user input."""

    db = SessionLocal()

    prompt = f"""
Return STRICT flat JSON ONLY.

Fields:
hcp_name, topics, sentiment, materials, samples, follow_up

Input:
{text}
"""

    raw = call_llm(prompt).strip()
    print("RAW CREATE:", raw)

    data = safe_parse_json(raw)

    clean = {}
    for key in ["hcp_name", "topics", "sentiment", "materials", "samples", "follow_up"]:
        val = data.get(key)
        if val and str(val).strip() != "":
            clean[key] = val

    if "sentiment" in clean:
        clean["sentiment"] = clean["sentiment"].capitalize()

    obj = Interaction(
        hcp_name=clean.get("hcp_name", ""),
        summary=clean.get("topics", ""),
        sentiment=clean.get("sentiment", ""),
        materials=clean.get("materials", ""),
        samples=clean.get("samples", ""),
        follow_up=clean.get("follow_up", ""),
        notes=text
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    print("DB SAVED:", obj.hcp_name, obj.summary, obj.sentiment)

    return clean


# -----------------------------
# EDIT TOOL
# -----------------------------
@tool
def edit_interaction_tool(text: str):
    """Update existing interaction fields safely."""

    db = SessionLocal()
    obj = db.query(Interaction).order_by(Interaction.id.desc()).first()

    if not obj:
        return {}

    prompt = f"""
Extract ONLY updated fields.

Return STRICT JSON ONLY.

Examples:
"Samples were 6 units" → {{"samples": "6 units"}}
"Sentiment was negative" → {{"sentiment": "Negative"}}

Allowed:
hcp_name, topics, sentiment, materials, samples, follow_up

Input:
{text}
"""

    raw = call_llm(prompt).strip()
    print("RAW EDIT:", raw)

    updates = safe_parse_json(raw)

    clean_updates = {}

    for k, v in updates.items():
        if v and str(v).strip() != "":
            clean_updates[k] = v

            # 🔥 MAP topics → summary column
            if k == "topics":
                setattr(obj, "summary", v)
            else:
                if hasattr(obj, k):
                    setattr(obj, k, v)

    if "sentiment" in clean_updates:
        clean_updates["sentiment"] = clean_updates["sentiment"].capitalize()
        obj.sentiment = clean_updates["sentiment"]

    db.commit()
    db.refresh(obj)

    print("DB UPDATED:", obj.hcp_name, obj.summary, obj.sentiment)

    return clean_updates


# -----------------------------
# SUMMARY TOOL
# -----------------------------
@tool
def summarize_tool(text: str):
    """Summarize latest interaction."""

    db = SessionLocal()
    obj = db.query(Interaction).order_by(Interaction.id.desc()).first()

    if not obj or not obj.hcp_name:
        return "No interaction found."

    context = f"""
Doctor: {obj.hcp_name}
Topics: {obj.summary}
Sentiment: {obj.sentiment}
Materials: {obj.materials}
Samples: {obj.samples}
"""

    print("SUMMARY CONTEXT:", context)

    prompt = f"""
Summarize this interaction accurately using ONLY the provided data.

{context}
"""

    return call_llm(prompt)


# -----------------------------
# EXTRACT TOOL
# -----------------------------
@tool
def extract_entities_tool(text: str):
    """Extract doctor and topics from latest interaction."""

    db = SessionLocal()
    obj = db.query(Interaction).order_by(Interaction.id.desc()).first()

    if not obj or not obj.hcp_name:
        return "No interaction found."

    return f"Doctor: {obj.hcp_name}, Topics: {obj.summary}"


# -----------------------------
# FOLLOW-UP TOOL
# -----------------------------
@tool
def followup_tool(text: str):
    """Suggest follow-up based on latest interaction."""

    db = SessionLocal()
    obj = db.query(Interaction).order_by(Interaction.id.desc()).first()

    if not obj or not obj.hcp_name:
        return "No interaction found."

    context = f"""
Doctor: {obj.hcp_name}
Topics: {obj.summary}
Sentiment: {obj.sentiment}
"""

    prompt = f"""
Based on this interaction, suggest a specific follow-up action.

{context}
"""

    return call_llm(prompt)