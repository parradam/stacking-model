from collections import defaultdict
from copy import deepcopy
from dataclasses import replace

from algorithm.domain.exceptions import PlacementError
from algorithm.domain.strategies import PutawayContext


def place_item(context: PutawayContext) -> PutawayContext:
    selected_placement = context.selected_placement

    if not selected_placement:
        msg = "No placement selected"
        raise PlacementError(msg)

    final_items = defaultdict(list, deepcopy(context.system.items))
    final_items[selected_placement].append(context.item)

    final_placement = selected_placement
    final_system = replace(context.system, items=final_items)
    return replace(context, system=final_system, final_placement=final_placement)
