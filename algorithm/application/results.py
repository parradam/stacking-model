from dataclasses import dataclass
from algorithm.domain.models import StorageSystem, Placement, Item


@dataclass(frozen=True)
class PutawayResult:
    storage_system: StorageSystem
    placement: Placement
    item: Item
