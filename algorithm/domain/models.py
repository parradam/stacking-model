from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional


@dataclass(frozen=True)
class Placement:
    x: int
    y: int
    z: int


@dataclass
class StorageSystemShape:
    name: str
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Item:
    id: str
    weight: Optional[float] = None


@dataclass()
class StorageSystem:
    shape: StorageSystemShape
    items: defaultdict[Placement, list[Item]] = field(
        default_factory=lambda: defaultdict(list)
    )
    max_weight: Optional[float] = None
