from fastapi import FastAPI
from events.router import router as events_router

app = FastAPI()

app.include_router(events_router, prefix="/events", tags=["events"])
