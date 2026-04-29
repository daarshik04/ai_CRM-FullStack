from sqlalchemy import Column, Integer, String, Text
from backend.app.db.session import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String)
    notes = Column(Text)
    summary = Column(Text)
    sentiment = Column(String)
    follow_up = Column(Text)