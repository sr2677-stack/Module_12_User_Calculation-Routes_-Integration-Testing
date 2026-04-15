from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, calculations

app = FastAPI(title="Calculation API", version="1.0.0")

app.include_router(users.router)
app.include_router(calculations.router)


@app.on_event("startup")
def startup():
    # Auto-create tables for demo/testing convenience.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
