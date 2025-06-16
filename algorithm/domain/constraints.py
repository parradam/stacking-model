from typing import Protocol

from algorithm.domain.exceptions import ItemMissingDataError, StorageSystemError
from algorithm.domain.models import Item, Placement, StorageSystem


def contains_none(*args: object) -> bool:
    """Check if any elements in the iterable are None."""
    return any(arg is None for arg in args)


class Constraint(Protocol):
    def apply(
        self,
        system: StorageSystem,
        placements: list[Placement],
        item: Item,
    ) -> list[Placement]: ...

    """Return the placements of items that satisfy the constraint."""


class MaxHeightConstraint:
    def __init__(self, max_height: int) -> None:
        self.max_z = max_height - 1

    def apply(
        self,
        _system: StorageSystem,
        placements: list[Placement],
        _item: Item,
    ) -> list[Placement]:
        return [placement for placement in placements if placement.z <= self.max_z]


class MaxItemWeightConstraint:
    def apply(
        self,
        system: StorageSystem,
        placements: list[Placement],
        item: Item,
    ) -> list[Placement]:
        constrained_placements: list[Placement] = []

        for placement in placements:
            if contains_none(system.max_weight, item.weight):
                raise ItemMissingDataError(item.id, "weight information")

            if system.max_weight is None:
                msg = "Storage system max_weight missing."
                raise StorageSystemError(msg)

            if item.weight is None:
                raise ItemMissingDataError(item.id, "weight information")

            if item.weight <= system.max_weight:
                constrained_placements.append(placement)
        return constrained_placements
