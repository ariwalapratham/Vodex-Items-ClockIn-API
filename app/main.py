from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import items_router, clock_in_router
from app.database import close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Items and User Clock-In Records API (Vodex.ai)",
    description="API for managing items and user clock-in records",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(items_router.router, prefix="/items", tags=["Items"])
app.include_router(clock_in_router.router, prefix="/clock-in", tags=["Clock-In"])