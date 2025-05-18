from algorithm.domain.models import Item, Placement, StorageSystem
from algorithm.domain.strategies import PlacementStrategy
from algorithm.domain.constraints import Constraint
from algorithm.domain.placement import place_item
from algorithm.domain.exceptions import PlacementError
from algorithm.application.results import PutawayResult


def putaway_item(
    storage_system: StorageSystem,
    strategy: PlacementStrategy,
    constraints: list[Constraint],
    item: Item,
) -> PutawayResult:
    candidate_placements: list[Placement] = strategy(storage_system)

    if not candidate_placements:
        raise PlacementError("No candidate placements available")

    # place item
    selected_placement = candidate_placements[0]
    updated_storage_system = place_item(storage_system, selected_placement, item)

    # return updated storage system
    return PutawayResult(updated_storage_system, selected_placement, item)
