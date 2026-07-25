"""Reusable FastAPI dependencies.

These ``Annotated`` aliases let endpoints declare ``service: ItemServiceDep``
and receive a ready-to-use service instance.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.services.item_service import ItemService


def get_item_service() -> ItemService:
    return ItemService()


ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
