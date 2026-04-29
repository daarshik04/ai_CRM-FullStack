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
hcp_name, topics, sentiment, materials, samples, outcomes, follow_up

Example:
Today I met Dr. Smith, discussed product X, shared brochure, distributed 3 samples, positive sentiment

Output:
{{
  "hcp_name": "Dr. Smith",
  "topics": "product X",
  "sentiment": "Positive",
  "materials": "brochure",
  "samples": "3 samples"
}}

Input:
{text}
"""

    raw = call_llm(prompt).strip()
    print("RAW CREATE:", raw)

    data = safe_parse_json(raw)

    clean = {}
    for key in ["hcp_name", "topics", "sentiment", "materials", "samples", "outcomes", "follow_up"]:
        val = data.get(key)
        if val and str(val).strip() != "":
            clean[key] = val

    if "sentiment" in clean:
        clean["sentiment"] = clean["sentiment"].capitalize()

    obj = Interaction(
        hcp_name=clean.get("hcp_name", ""),
        notes=text,
        summary=clean.get("topics", ""),
        sentiment=clean.get("sentiment", ""),
        follow_up=clean.get("follow_up", "")
    )

    db.add(obj)
    db.commit()

    return clean


# -----------------------------
# EDIT TOOL
# -----------------------------
@tool
def edit_interaction_tool(text: str):
    """Update existing interaction fields safely."""

    db = SessionLocal()
    obj = db.query(Interaction).first()

    if not obj:
        return {}

    prompt = f"""
Extract ONLY updated fields.

Return STRICT JSON ONLY.

Examples:
"Samples were 6 units" → {{"samples": "6 units"}}
"Sentiment was negative" → {{"sentiment": "Negative"}}

Allowed:
hcp_name, topics, sentiment, materials, samples, outcomes, follow_up

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
            if hasattr(obj, k):
                setattr(obj, k, v)

    if "sentiment" in clean_updates:
        clean_updates["sentiment"] = clean_updates["sentiment"].capitalize()

    db.commit()

    return clean_updates


# -----------------------------
# SUMMARIZE TOOL
# -----------------------------
@tool
def summarize_tool(text: str):
    """Summarize latest interaction."""

    db = SessionLocal()
    obj = db.query(Interaction).first()

    if not obj:
        return "No interaction found."

    context = f"""
Doctor: {obj.hcp_name}
Topics: {obj.summary}
Sentiment: {obj.sentiment}
Follow up: {obj.follow_up}
"""

    return call_llm(f"Summarize this interaction:\n{context}")


# -----------------------------
# EXTRACT TOOL
# -----------------------------
@tool
def extract_entities_tool(text: str):
    """Extract entities from latest interaction."""

    db = SessionLocal()
    obj = db.query(Interaction).first()

    if not obj:
        return "No interaction found."

    context = f"""
Doctor: {obj.hcp_name}
Topics: {obj.summary}
"""

    return call_llm(f"Extract doctor and topics:\n{context}")


# -----------------------------
# FOLLOW-UP TOOL
# -----------------------------
@tool
def followup_tool(text: str):
    """Suggest follow-up."""
    return call_llm(f"Suggest next follow-up:\n{text}")