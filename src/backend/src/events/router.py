"""Main Events Router for the Open Baby Backend."""

from fastapi import APIRouter
import structlog

router = APIRouter()

log = structlog.get_logger()


@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify the router is working."""
    log.info("Test endpoint hit")
    return {"message": "Test successful"}
