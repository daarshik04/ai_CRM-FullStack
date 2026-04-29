from pydantic import BaseModel

class InteractionCreate(BaseModel):
    hcp_name: str
    notes: str