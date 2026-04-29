from fastapi import APIRouter
from backend.app.agents.graph import run_agent
from datetime import datetime
import pytz
import json

router = APIRouter()


def add_current_datetime(data):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)

    data["date"] = now.strftime("%Y-%m-%d")
    data["time"] = now.strftime("%H:%M")

    return data


@router.post("/chat")
def chat(query: str):
    result = run_agent(query)

    data = result.get("result")

    print("RAW RESULT FROM AGENT:", data)

    if isinstance(data, dict):
        return add_current_datetime(data)

    try:
        parsed = json.loads(data)
        return add_current_datetime(parsed)
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        return {"error": "Invalid JSON from AI"}