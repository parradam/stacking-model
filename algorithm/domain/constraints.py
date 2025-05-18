from typing import Protocol
from .models import StorageSystem, Placement, Item


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
