from dataclasses import dataclass, field

from src.domain.item import Item
from src.domain.placement import Placement
from src.domain.storage_system import StorageSystem


@dataclass
class PutawayContext:
    system: StorageSystem
    item: Item
    selected_placement: Placement | None = None
    final_placement: Placement | None = None
    placements: list[Placement] = field(default_factory=list[Placement])
    invalid_placements: list[Placement] = field(default_factory=list[Placement])
