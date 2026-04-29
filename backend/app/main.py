from fastapi import FastAPI
from backend import app
from backend.app.db.session import Base, engine
from backend.app.models import interaction

from backend.app.api.v1 import interaction as interaction_api
from backend.app.api.v1 import ai as ai_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# create tables
Base.metadata.create_all(bind=engine)

# routes
app.include_router(interaction_api.router, prefix="/api/v1/interactions")
app.include_router(ai_api.router, prefix="/api/v1/ai")


@app.get("/")
def root():
    return {"message": "AI CRM running"}