from fastapi import FastAPI
from events.router import router as events_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://192.168.1.204:3000",
        "http://192.168.1.204:3000/",
    ],  # TODO: Make this configurable
    allow_credentials=True,
    allow_methods=["GET", "PUT", "PATCH", "DELETE", "POST"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(events_router, prefix="/events", tags=["events"])
