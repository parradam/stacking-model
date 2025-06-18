from dataclasses import dataclass

from algorithm.domain.exceptions import ItemMissingDataError, StorageSystemError
from algorithm.domain.models import Item, Placement, StorageSystem


@dataclass
class ConstraintConfig:
    system: StorageSystem
    placements: list[Placement]
    item: Item


def _contains_none(*args: object) -> bool:
    """Check if any elements in the iterable are None."""
    return any(arg is None for arg in args)


def apply_max_height_constraint(
    config: ConstraintConfig,
    max_z: int,
) -> list[Placement]:
    return [p for p in config.placements if p.z <= max_z]


def apply_max_item_weight_constraint(config: ConstraintConfig) -> list[Placement]:
    system = config.system
    placements = config.placements
    item = config.item

    constrained_placements: list[Placement] = []

    for placement in placements:
        if _contains_none(config.system.max_weight, item.weight):
            raise ItemMissingDataError(item.id, "weight information")

        if system.max_weight is None:
            msg = "Storage system max_weight missing."
            raise StorageSystemError(msg)

        if item.weight is None:
            raise ItemMissingDataError(item.id, "weight information")

        if item.weight <= system.max_weight:
            constrained_placements.append(placement)
    return constrained_placements
