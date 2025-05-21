from typing import Protocol
from algorithm.domain.models import StorageSystem, Placement, Item
from algorithm.domain.exceptions import ItemMissingDataError
from typing import Any


def contains_none(*args: Any) -> bool:
    """Check if any elements in the iterable are None."""
    return any(arg is None for arg in args)


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
        constrained_placements: list[Placement] = []

        for placement in placements:
            if placement.z <= self.max_z:
                constrained_placements.append(placement)
        return constrained_placements


class MaxItemWeightConstraint:
    def apply(
        self, system: StorageSystem, placements: list[Placement], item: Item
    ) -> list[Placement]:
        constrained_placements: list[Placement] = []

        for placement in placements:
            if contains_none(system.max_weight, item.weight):
                raise ItemMissingDataError(item.id, "weight information")

            assert system.max_weight is not None and item.weight is not None

            if item.weight <= system.max_weight:
                constrained_placements.append(placement)
        return constrained_placements
