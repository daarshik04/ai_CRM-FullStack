from sqlalchemy import Column, Integer, String, Text
from backend.app.db.session import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_name = Column(String)
    summary = Column(String)       # topics
    sentiment = Column(String)
    materials = Column(String)
    samples = Column(String)
    follow_up = Column(String)

    notes = Column(Text)           # raw input