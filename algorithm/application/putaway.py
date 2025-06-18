from algorithm.application.results import PutawayResult
from algorithm.domain.constraints import Constraint
from algorithm.domain.exceptions import PlacementError
from algorithm.domain.models import Item, Placement, StorageSystem
from algorithm.domain.placement import place_item
from algorithm.domain.strategies import PlacementStrategy


def putaway_item(
    storage_system: StorageSystem,
    strategy: PlacementStrategy,
    _constraints: list[Constraint],
    item: Item,
) -> PutawayResult:
    candidate_placements: list[Placement] = strategy(storage_system)

    if not candidate_placements:
        msg = "No candidate placements available"
        raise PlacementError(msg)

    selected_placement = candidate_placements[0]
    updated_storage_system = place_item(storage_system, selected_placement, item)

    return PutawayResult(updated_storage_system, selected_placement, item)
