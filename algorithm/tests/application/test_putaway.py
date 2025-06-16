from typing import TYPE_CHECKING

import pytest

from algorithm.application.putaway import putaway_item
from algorithm.domain.exceptions import PlacementError
from algorithm.domain.models import Item, StorageSystem, StorageSystemShape
from algorithm.domain.strategies import VerticalPlacementStrategy

if TYPE_CHECKING:
    from algorithm.domain.constraints import Constraint


def test_can_putaway_one_item_() -> None:
    storage_system_shape = StorageSystemShape("test_system", 3, 3, 3)
    storage_system = StorageSystem(
        shape=storage_system_shape,
    )
    strategy = VerticalPlacementStrategy()
    constraints: list[Constraint] = []
    item1 = Item("item1")

    assert storage_system.items == {}

    result = putaway_item(
        storage_system=storage_system,
        strategy=strategy,
        _constraints=constraints,
        item=item1,
    )

    updated_storage_system = result.storage_system
    placement = result.placement
    assert len(updated_storage_system.items) == 1
    assert updated_storage_system.items[placement] == [item1]


def test_can_putaway_until_full() -> None:
    storage_system_shape = StorageSystemShape("test_system", 2, 2, 2)
    storage_system = StorageSystem(
        shape=storage_system_shape,
    )
    strategy = VerticalPlacementStrategy()
    constraints: list[Constraint] = []
    items = [Item(f"item{i}") for i in range(8)]

    assert storage_system.items == {}

    for item in items:
        result = putaway_item(
            storage_system=storage_system,
            strategy=strategy,
            _constraints=constraints,
            item=item,
        )
        storage_system = result.storage_system

    # check all 8 items in storage system
    assert len(storage_system.items) == len(items)


def test_putaway_when_full_raises_exception() -> None:
    storage_system_shape = StorageSystemShape("test_system", 2, 2, 2)
    storage_system = StorageSystem(
        shape=storage_system_shape,
    )
    strategy = VerticalPlacementStrategy()
    constraints: list[Constraint] = []
    items = [Item(f"item{i}") for i in range(9)]

    assert storage_system.items == {}

    # put away 8 items
    for item in items[:8]:
        result = putaway_item(
            storage_system=storage_system,
            strategy=strategy,
            _constraints=constraints,
            item=item,
        )
        storage_system = result.storage_system

    # try to put away the 9th item
    with pytest.raises(PlacementError):
        putaway_item(
            storage_system=storage_system,
            strategy=strategy,
            _constraints=constraints,
            item=items[-1],
        )

    # check only 8 items in storage system
    assert len(storage_system.items) == len(items) - 1
