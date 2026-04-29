

from backend.app.services.groq_services import call_llm
from backend.app.db.session import SessionLocal
from backend.app.models.interaction import Interaction


def log_interaction_tool(text: str):
    db = SessionLocal()

    prompt = f"""
You are an AI assistant for a CRM system.

Your task is to extract structured data from user input.

IMPORTANT RULES:

1. Return ONLY valid JSON. No explanation, no text outside JSON.

2. You must support TWO modes automatically:

   A) CREATE MODE:
   - If user describes a full interaction
   - Extract ALL relevant fields

   B) EDIT MODE:
   - If user corrects or updates something
   - Extract ONLY the fields being updated
   - DO NOT include unchanged fields

3. Allowed fields:
- hcp_name
- topics
- sentiment (Positive, Neutral, Negative)
- outcomes
- follow_up
- date (YYYY-MM-DD if explicitly mentioned)
- time (HH:MM 24-hour format if explicitly mentioned)

4. DO NOT:
- Do not invent values
- Do not include empty fields
- Do not include fields not mentioned (in edit mode)

5. If time is mentioned:
- Convert to 24-hour format
- Example: "1.20 PM" → "13:20"
- Example: "3 PM" → "15:00"

---

EXAMPLES:

Input:
"Today I met Dr. Smith, discussed product efficacy, positive sentiment"

Output:
{{
  "hcp_name": "Dr. Smith",
  "topics": "product efficacy",
  "sentiment": "Positive"
}}

---

Input:
"Actually sentiment is negative"

Output:
{{
  "sentiment": "Negative"
}}

---

Input:
"Sorry name is Dr. John and time was 1.20 PM"

Output:
{{
  "hcp_name": "Dr. John",
  "time": "13:20"
}}

---

Now process this input:

{text}
"""

    structured = call_llm(prompt)

    # ⚠️ IMPORTANT: we don't trust parsing fully → just store raw for now
    obj = Interaction(
        hcp_name="AI Parsed",
        notes=text,
        summary=structured
    )

    db.add(obj)
    db.commit()

    return structured


def edit_interaction_tool(id: int, text: str):
    db = SessionLocal()
    obj = db.query(Interaction).filter(Interaction.id == id).first()

    if obj:
        obj.notes = text
        db.commit()
        return {"message": "updated"}

    return {"error": "not found"}


def summarize_tool(text: str):
    return call_llm(f"Summarize:\n{text}")


def extract_entities_tool(text: str):
    return call_llm(f"Extract doctor + topics:\n{text}")


def followup_tool(text: str):
    return call_llm(f"Suggest follow-up:\n{text}")