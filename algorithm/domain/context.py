from dataclasses import dataclass, field

from algorithm.domain.item import Item
from algorithm.domain.placement import Placement
from algorithm.domain.storage_system import StorageSystem


@dataclass
class PutawayContext:
    system: StorageSystem
    item: Item
    selected_placement: Placement | None = None
    final_placement: Placement | None = None
    placements: list[Placement] = field(default_factory=list[Placement])
    invalid_placements: list[Placement] = field(default_factory=list[Placement])
