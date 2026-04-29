from fastapi import APIRouter
from backend.app.agents.graph import run_agent
import json

router = APIRouter()

from datetime import datetime
import pytz

def add_current_datetime(data):
    # use local timezone (change if needed)
    tz = pytz.timezone("Asia/Kolkata")  # or your timezone
    now = datetime.now(tz)

    data["date"] = now.strftime("%Y-%m-%d")
    data["time"] = now.strftime("%H:%M")

    return data


@router.post("/chat")
def chat(query: str):
    result = run_agent(query)

    try:
        parsed = json.loads(result["result"])
        parsed = add_current_datetime(parsed)
        return parsed
    except:
        return {"error": "Invalid JSON"}
    
    