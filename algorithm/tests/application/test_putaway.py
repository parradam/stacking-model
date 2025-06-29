import pytest

from algorithm.application.putaway import putaway_item
from algorithm.domain.item import Item
from algorithm.domain.placement import PlacementError
from algorithm.domain.storage_system import (
    StorageSystem,
    StorageSystemShape,
)
from algorithm.domain.strategies import PutawayContext


class TestPutaway:
    def test_one_item(self) -> None:
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 3, 3, 3),
        )
        item = Item("item1")

        assert system.items == {}

        input_context = PutawayContext(system=system, item=item)
        output_context = putaway_item(input_context)

        final_placement = output_context.final_placement

        assert final_placement
        assert output_context.system.items[final_placement] == item

    def test_works_until_full(self) -> None:
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 2, 2, 2),
        )
        items = [Item(f"item{i}") for i in range(8)]

        assert system.items == {}

        for item in items:
            context = PutawayContext(system=system, item=item)
            result = putaway_item(context=context)
            system = result.system

        # check all 8 items in storage system
        assert len(system.items) == len(items)

    def test_raises_exception_when_full(self) -> None:
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 2, 2, 2),
        )
        items = [Item(f"item{i}") for i in range(9)]

        assert system.items == {}

        # put away 8 items
        for item in items[:8]:
            context = PutawayContext(system=system, item=item)
            result = putaway_item(context=context)
            system = result.system

        # try to put away the 9th item
        context = PutawayContext(system=system, item=items[-1])
        with pytest.raises(PlacementError):
            putaway_item(context=context)

        # check only 8 items in storage system
        assert len(system.items) == len(items) - 1
