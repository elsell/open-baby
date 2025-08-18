"""Main Events Router for the Open Baby Backend."""

from fastapi import APIRouter
import structlog

from events.feed.router import router as feed_router

router = APIRouter()

log = structlog.get_logger()

router.include_router(feed_router, prefix="/feed", tags=["feed"])
