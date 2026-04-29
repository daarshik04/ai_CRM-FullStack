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


# ---------------------------------------
# CREATE TOOL
# ---------------------------------------
def log_interaction_tool(text: str):
    db = SessionLocal()

    prompt = f"""
You are a data extraction engine.

Return STRICT JSON ONLY.
No explanation. No extra text.

Example:
{{"hcp_name": "Dr. Smith", "topics": "product X", "sentiment": "Positive"}}

Input:
{text}
"""

    structured = call_llm(prompt).strip()
    print("\nRAW LLM OUTPUT (CREATE):", structured)

    data = safe_parse_json(structured)

    # 🔥 fallback so system NEVER breaks
    if not data:
        data = {
            "hcp_name": "",
            "topics": text,
            "sentiment": "Neutral",
            "outcomes": "",
            "follow_up": ""
        }

    # 🔥 FIX: Normalize sentiment
    if "sentiment" in data and isinstance(data["sentiment"], str):
        data["sentiment"] = data["sentiment"].capitalize()

    obj = Interaction(
        hcp_name=data.get("hcp_name", ""),
        notes=text,
        summary=data.get("topics", ""),
        sentiment=data.get("sentiment", ""),
        follow_up=data.get("follow_up", "")
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return data


# ---------------------------------------
# EDIT TOOL
# ---------------------------------------
def edit_interaction_tool(id: int, text: str):
    db = SessionLocal()
    obj = db.query(Interaction).filter(Interaction.id == id).first()

    if not obj:
        return {}

    prompt = f"""
Extract ONLY updated fields.

Return STRICT JSON ONLY.

Example:
{{"sentiment": "Negative"}}

Input:
{text}
"""

    structured = call_llm(prompt).strip()
    print("\nRAW LLM OUTPUT (EDIT):", structured)

    updates = safe_parse_json(structured)

    # 🔥 fallback so edit never breaks UI
    if not updates:
        return {}

    # 🔥 FIX: Normalize sentiment
    if "sentiment" in updates and isinstance(updates["sentiment"], str):
        updates["sentiment"] = updates["sentiment"].capitalize()

    for key, value in updates.items():
        if hasattr(obj, key) and value:
            setattr(obj, key, value)

    db.commit()

    return updates


# ---------------------------------------
# OTHER TOOLS
# ---------------------------------------
def summarize_tool(text: str):
    return call_llm(f"Summarize this interaction:\n{text}")


def extract_entities_tool(text: str):
    return call_llm(f"Extract doctor name and key topics:\n{text}")


def followup_tool(text: str):
    return call_llm(f"Suggest next best follow-up:\n{text}")