from dataclasses import dataclass, field, replace
from enum import Enum

from algorithm.domain.exceptions import (
    ConstraintError,
    ItemMissingDataError,
    StorageSystemError,
)
from algorithm.domain.models import Item, Placement, StorageSystem
from algorithm.domain.strategies import PutawayContext


class ConstraintStatus(Enum):
    ENABLED = 0
    DISABLED = 1


@dataclass
class ConstraintContext:
    system: StorageSystem
    placements: list[Placement]
    item: Item
    invalid_placements: list[Placement] = field(default_factory=list[Placement])


def _contains_none(*args: object) -> bool:
    """Check if any elements in the iterable are None."""
    return any(arg is None for arg in args)


def apply_max_height_constraint(
    context: PutawayContext,
    max_height: int | None = None,
    status: ConstraintStatus = ConstraintStatus.DISABLED,
) -> PutawayContext:
    if status == ConstraintStatus.DISABLED:
        return context

    if max_height is None:
        msg = "max_height not specified"
        raise ConstraintError(msg)

    valid_placements = [p for p in context.placements if p.z < max_height]
    invalid_placements = context.invalid_placements + [
        p for p in context.placements if p not in valid_placements
    ]

    return replace(
        context,
        placements=valid_placements,
        invalid_placements=invalid_placements,
    )


def apply_max_item_weight_constraint(
    context: PutawayContext,
    status: ConstraintStatus = ConstraintStatus.DISABLED,
) -> PutawayContext:
    if status == ConstraintStatus.DISABLED:
        return context

    system = context.system
    placements = context.placements
    item = context.item

    valid_placements: list[Placement] = []
    invalid_placements: list[Placement] = []
    invalid_placements += context.invalid_placements

    # TODO(parradam): rather than raising Exceptions, add to a warnings variable
    # TODO(parradam): subdivide warnings with flag (in/out dataset dep on config)
    for placement in placements:
        if _contains_none(context.system.max_weight, item.weight):
            raise ItemMissingDataError(item.id, "weight information")

        if system.max_weight is None:
            msg = "Storage system max_weight missing."
            raise StorageSystemError(msg)

        if item.weight is None:
            raise ItemMissingDataError(item.id, "weight information")

        if item.weight <= system.max_weight:
            valid_placements.append(placement)
        else:
            invalid_placements.append(placement)

    return replace(
        context,
        placements=valid_placements,
        invalid_placements=invalid_placements,
    )
