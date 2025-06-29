from dataclasses import dataclass, field

from algorithm.domain.item import Item
from algorithm.domain.placement import Placement


class StorageSystemError(Exception):
    """Base class for all exceptions related to the storage system."""


@dataclass
class StorageSystemShape:
    name: str
    x: int
    y: int
    z: int


@dataclass
class StorageSystem:
    shape: StorageSystemShape
    items: dict[Placement, Item] = field(default_factory=dict[Placement, Item])
    max_weight: float | None = None
