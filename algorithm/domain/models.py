from collections import defaultdict
from dataclasses import dataclass, field


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
    weight: float | None = None


@dataclass()
class StorageSystem:
    shape: StorageSystemShape
    items: defaultdict[Placement, list[Item]] = field(
        default_factory=lambda: defaultdict(list),
    )
    max_weight: float | None = None
