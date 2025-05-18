from typing import Protocol
from algorithm.domain.models import StorageSystem, Placement


class PlacementStrategy(Protocol):
    def __call__(self, storage_system: StorageSystem) -> list[Placement]: ...


class VerticalPlacementStrategy:
    def __call__(self, storage_system: StorageSystem) -> list[Placement]:
        """
        Get candidate placements for the vertical stacking strategy.
        This strategy finds the first available placement for each (x, y) coordinate.
        """

        shape = storage_system.shape
        occupied = storage_system.items.keys()

        def _next_vertical_space_in_stack(x: int, y: int) -> int | None:
            """Find the lowest free z-coordinate for a given (x, y) coordinate."""
            for z in range(shape.z):
                if Placement(x, y, z) not in occupied:
                    return z
            return None

        candidate_placements: list[Placement] = []
        for x in range(shape.x):
            for y in range(shape.y):
                z = _next_vertical_space_in_stack(x, y)
                if z is not None:
                    candidate_placements.append(Placement(x, y, z))

        return candidate_placements
