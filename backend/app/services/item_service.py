"""Item business logic with an in-memory store.

No database — this keeps the layered structure (endpoint -> service) intact so
swapping in a real datastore later is a localized change. The store is a module
-level dict; it resets on restart and is not safe across multiple workers.
"""

from __future__ import annotations

from itertools import count

from app.core.exceptions import NotFoundError
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

# Process-local store. Replace with a real datastore for persistence.
_items: dict[int, ItemRead] = {}
_id_seq = count(1)


class ItemService:
    def list_items(self) -> list[ItemRead]:
        return list(_items.values())

    def get_item(self, item_id: int) -> ItemRead:
        item = _items.get(item_id)
        if item is None:
            raise NotFoundError("Item not found.")
        return item

    def create_item(self, payload: ItemCreate) -> ItemRead:
        item = ItemRead(id=next(_id_seq), **payload.model_dump())
        _items[item.id] = item
        return item

    def update_item(self, item_id: int, payload: ItemUpdate) -> ItemRead:
        item = self.get_item(item_id)
        updated = item.model_copy(update=payload.model_dump(exclude_unset=True))
        _items[item_id] = updated
        return updated

    def delete_item(self, item_id: int) -> None:
        if item_id not in _items:
            raise NotFoundError("Item not found.")
        del _items[item_id]
