from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, calculations


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Auto-create tables for demo/testing convenience.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Calculation API", version="1.0.0", lifespan=lifespan)

app.include_router(users.router)
app.include_router(calculations.router)


@app.get("/health")
def health():
    return {"status": "ok"}
