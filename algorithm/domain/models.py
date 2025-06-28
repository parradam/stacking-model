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
    items: dict[Placement, Item] = field(default_factory=dict[Placement, Item])
    max_weight: float | None = None
