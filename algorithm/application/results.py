from dataclasses import dataclass

from algorithm.domain.models import Item, Placement, StorageSystem


@dataclass(frozen=True)
class PutawayResult:
    storage_system: StorageSystem
    placement: Placement
    item: Item
