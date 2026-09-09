"""Integration tests for health and the item CRUD flow."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_health(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


async def test_item_crud(client: AsyncClient) -> None:
    created = await client.post("/api/v1/items", json={"name": "Widget", "description": "A thing"})
    assert created.status_code == 201, created.text
    item = created.json()
    item_id = item["id"]
    assert item["name"] == "Widget"

    fetched = await client.get(f"/api/v1/items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == item_id

    updated = await client.patch(f"/api/v1/items/{item_id}", json={"name": "Gadget"})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Gadget"

    deleted = await client.delete(f"/api/v1/items/{item_id}")
    assert deleted.status_code == 204

    missing = await client.get(f"/api/v1/items/{item_id}")
    assert missing.status_code == 404


async def test_item_validation_error(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/items", json={"name": ""})
    assert resp.status_code == 422
