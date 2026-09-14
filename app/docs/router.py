from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.docs import templates

router = APIRouter(tags=["documentation"])


@router.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def docs_overview():
    """API documentation — overview page."""
    return templates.overview()


@router.get("/docs/groq", response_class=HTMLResponse, include_in_schema=False)
async def docs_groq():
    """API documentation — Groq provider page."""
    return templates.groq()


@router.get("/docs/sarvam", response_class=HTMLResponse, include_in_schema=False)
async def docs_sarvam():
    """API documentation — Sarvam provider page."""
    return templates.sarvam()
