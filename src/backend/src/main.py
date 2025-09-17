from fastapi import FastAPI
from events.router import router as events_router
from stats.router import router as stats_router
from fastapi.middleware.cors import CORSMiddleware
from config import config
from structlog import get_logger

logger = get_logger()

app = FastAPI(root_path=config.root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "PATCH", "DELETE", "POST"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

logger.info("CORS middleware configured", allow_origins=config.allow_origins)

app.include_router(events_router, prefix="/events", tags=["events"])
app.include_router(stats_router, prefix="/stats", tags=["stats"])
