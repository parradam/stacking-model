from dataclasses import replace

from src.domain.place_item import place_item
from src.domain.placement import PlacementError
from src.domain.strategies import (
    PutawayContext,
    get_vertical_placements_for_putaway,
)


def putaway_item(
    context: PutawayContext,
) -> PutawayContext:
    context = get_vertical_placements_for_putaway(context)

    if not context.placements:
        msg = "No candidate placements available"
        raise PlacementError(msg)

    # TODO(parradam): add logic to select best location (decoupled from actual putaway)
    selected_placement = context.placements[0]
    context_with_selected_placement = replace(
        context,
        selected_placement=selected_placement,
    )

    return place_item(context_with_selected_placement)
