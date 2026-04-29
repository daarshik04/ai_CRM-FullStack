from fastapi import APIRouter
from backend.app.agents.graph import run_agent
from datetime import datetime
import pytz

router = APIRouter()


@router.post("/chat")
def chat(query: str):
    result = run_agent(query)

    raw = result.get("result", {})

    print("RAW RESULT:", raw)

    # Structured response (form fill)
    if isinstance(raw, dict):
        tz = pytz.timezone("Asia/Kolkata")
        now = datetime.now(tz)

        raw["date"] = now.strftime("%Y-%m-%d")
        raw["time"] = now.strftime("%H:%M")

        return raw

    # Text response (summarize / extract / followup)
    return {"message": raw}