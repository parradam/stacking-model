from dataclasses import dataclass, field, replace

from algorithm.domain.models import Item, Placement, StorageSystem


@dataclass
class PutawayContext:
    system: StorageSystem
    item: Item
    selected_placement: Placement | None = None
    final_placement: Placement | None = None
    placements: list[Placement] = field(default_factory=list[Placement])
    invalid_placements: list[Placement] = field(default_factory=list[Placement])


def get_vertical_placements_for_putaway(context: PutawayContext) -> PutawayContext:
    """
    Get candidate placements for the vertical stacking strategy.
    This strategy finds the first available placement for each (x, y) coordinate.
    """

    def _next_vertical_space_in_stack(x: int, y: int) -> int | None:
        """Find the lowest free z-coordinate for a given (x, y) coordinate."""
        for z in range(shape.z):
            if Placement(x, y, z) not in occupied:
                return z
        return None

    shape = context.system.shape
    occupied = context.system.items.keys()

    candidate_placements: list[Placement] = []
    for x in range(shape.x):
        for y in range(shape.y):
            z = _next_vertical_space_in_stack(x, y)
            if z is not None:
                candidate_placements.append(Placement(x, y, z))

    return replace(context, placements=candidate_placements)
