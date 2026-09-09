"""Liveness probe."""

from __future__ import annotations

from fastapi import APIRouter, Response, status

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health check")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": settings.VERSION}


@router.get("/live", status_code=status.HTTP_204_NO_CONTENT, summary="Kubernetes liveness")
async def live() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
