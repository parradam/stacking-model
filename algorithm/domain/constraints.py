from typing import Protocol
from algorithm.domain.models import StorageSystem, Placement, Item
from algorithm.domain.exceptions import ItemMissingDataError
from typing import Any



class Constraint(Protocol):
    def apply(
        self, system: StorageSystem, placements: list[Placement], item: Item
    ) -> list[Placement]: ...

    """Return the placements of items that satisfy the constraint."""


class MaxHeightConstraint:
    def __init__(self, max_height: int):
        self.max_z = max_height - 1

    def apply(
        self, system: StorageSystem, placements: list[Placement], item: Item
    ) -> list[Placement]:
        return [
            placement
            for placement in placements
            if placement.z <= self.max_z
        ]


class MaxItemWeightConstraint:
    def apply(
        self, system: StorageSystem, placements: list[Placement], item: Item
    ) -> list[Placement]:
        constrained_placements: list[Placement] = []

        for placement in placements:
            if _contains_none(system.max_weight, item.weight):
                raise ItemMissingDataError(item.id, "weight information")

            # XXX: avoid assert anywhere in non-test code
            assert system.max_weight is not None and item.weight is not None

            if item.weight <= system.max_weight:
                constrained_placements.append(placement)
        
        return constrained_placements


def _contains_none(*args: Any) -> bool:
    """Check if any elements in the iterable are None."""
    return any(arg is None for arg in args)


"""
@dataclass
class ConstraintConfig:
    system: StorageSystem
    placements: list[Placement]
    item: Item

def apply_max_height_constraint(
    constraint_config: ConstraintConfig, max_z
) -> list[Placement]:
    constrained_placements: list[Placement] = []

    # for placement in placements:
    #     if placement.z <= self.max_z:
    #         constrained_placements.append(placement)
    return constrained_placements


def apply_max_item_height_constraint(
    constraint_config: ConstraintConfig,
) -> list[Placement]:
    constrained_placements: list[Placement] = []

    # for placement in placements:
    #     if placement.z <= self.max_z:
    #         constrained_placements.append(placement)
    return constrained_placements

"""