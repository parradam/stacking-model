from src.domain.context import PutawayContext
from src.domain.item import Item
from src.domain.placement import Placement
from src.domain.storage_system import (
    StorageSystem,
    StorageSystemShape,
)
from src.domain.strategies import get_vertical_placements_for_putaway


class TestVerticalPlacementStrategy:
    def test_finds_candidates(self) -> None:
        # A list of placements for an empty 4x3x2 storage system
        expected_placements = [
            Placement(0, 0, 0),
            Placement(0, 1, 0),
            Placement(0, 2, 0),
            Placement(1, 0, 0),
            Placement(1, 1, 0),
            Placement(1, 2, 0),
            Placement(2, 0, 0),
            Placement(2, 1, 0),
            Placement(2, 2, 0),
            Placement(3, 0, 0),
            Placement(3, 1, 0),
            Placement(3, 2, 0),
        ]
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 4, 3, 2),
        )
        item = Item("item99")

        input_context = PutawayContext(system=system, item=item)
        output_context = get_vertical_placements_for_putaway(input_context)

        assert output_context.placements == expected_placements

    def test_finds_candidates_with_items(self) -> None:
        # A list of placements for a 4x3x2 storage system with some items
        expected_placements = [
            Placement(0, 0, 0),
            Placement(0, 1, 0),
            Placement(0, 2, 1),  # one item below
            Placement(1, 0, 0),
            Placement(1, 1, 0),
            Placement(1, 2, 0),
            Placement(2, 0, 0),
            Placement(2, 1, 0),
            Placement(2, 2, 0),
            Placement(3, 1, 0),
            Placement(3, 2, 0),
        ]
        items_placements = {
            "item1": Placement(0, 2, 0),
            "item2": Placement(3, 0, 0),
            "item3": Placement(3, 0, 1),
        }
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 4, 3, 2),
        )
        for item, placement in items_placements.items():
            system.items[placement] = Item(item)
        new_item = Item("item99")

        input_context = PutawayContext(system=system, item=new_item)
        output_context = get_vertical_placements_for_putaway(input_context)

        assert output_context.placements == expected_placements

    def test_finds_no_candidates_if_full(self) -> None:
        items_placements = {
            "item1": Placement(0, 0, 0),
            "item2": Placement(0, 0, 1),
            "item3": Placement(0, 1, 0),
            "item4": Placement(0, 1, 1),
            "item5": Placement(1, 0, 0),
            "item6": Placement(1, 0, 1),
            "item7": Placement(1, 1, 0),
            "item8": Placement(1, 1, 1),
        }
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 2, 2, 2),
        )
        for item, placement in items_placements.items():
            system.items[placement] = Item(item)
        new_item = Item("item99")

        input_context = PutawayContext(system=system, item=new_item)
        output_context = get_vertical_placements_for_putaway(input_context)

        assert len(output_context.placements) == 0
