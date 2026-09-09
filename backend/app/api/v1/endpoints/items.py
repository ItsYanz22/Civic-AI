"""Item CRUD endpoints (in-memory, no database)."""

from __future__ import annotations

from fastapi import APIRouter, Response, status

from app.api.v1.dependencies.common import ItemServiceDep
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead], summary="List items")
async def list_items(service: ItemServiceDep) -> list[ItemRead]:
    return service.list_items()


@router.post(
    "",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
)
async def create_item(payload: ItemCreate, service: ItemServiceDep) -> ItemRead:
    return service.create_item(payload)


@router.get("/{item_id}", response_model=ItemRead, summary="Get an item by id")
async def get_item(item_id: int, service: ItemServiceDep) -> ItemRead:
    return service.get_item(item_id)


@router.patch("/{item_id}", response_model=ItemRead, summary="Update an item")
async def update_item(item_id: int, payload: ItemUpdate, service: ItemServiceDep) -> ItemRead:
    return service.update_item(item_id, payload)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
async def delete_item(item_id: int, service: ItemServiceDep) -> Response:
    service.delete_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
