from dataclasses import dataclass


class ItemError(Exception):
    """Base class for all exceptions related to items."""


class ItemMissingDataError(ItemError):
    """Exception raised when an item is missing data."""

    def __init__(self, item_id: str, missing_data: str) -> None:
        super().__init__(f"Item {item_id} is missing data: {missing_data}.")
        self.item_id = item_id
        self.missing_data = missing_data


@dataclass(frozen=True)
class Item:
    id: str
    weight: float | None = None
