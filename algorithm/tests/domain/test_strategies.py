from algorithm.domain.models import Item, Placement, StorageSystem, StorageSystemShape
from algorithm.domain.strategies import VerticalPlacementStrategy


def test_vertical_placement_strategy_finds_candidates() -> None:
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

    storage_system = StorageSystem(
        shape=StorageSystemShape("test_system", 4, 3, 2),
    )

    strategy = VerticalPlacementStrategy()
    candidate_placements = strategy(storage_system)

    assert candidate_placements == expected_placements


def test_vertical_placement_strategy_finds_candidates_with_items() -> None:
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

    items_and_placements = [
        (Item("item1"), Placement(0, 2, 0)),
        (Item("item2"), Placement(3, 0, 0)),
        (Item("item3"), Placement(3, 0, 1)),
    ]

    storage_system_shape = StorageSystemShape("test_system", 4, 3, 2)
    storage_system = StorageSystem(
        shape=storage_system_shape,
    )
    for item, placement in items_and_placements:
        storage_system.items[placement].append(item)

    strategy = VerticalPlacementStrategy()
    candidate_placements = strategy(storage_system)

    assert candidate_placements == expected_placements


def test_vertical_placement_strategy_finds_no_candidates_if_full() -> None:
    items_and_placements = [
        (Item("item1"), Placement(0, 0, 0)),
        (Item("item2"), Placement(0, 0, 1)),
        (Item("item3"), Placement(0, 1, 0)),
        (Item("item4"), Placement(0, 1, 1)),
        (Item("item5"), Placement(1, 0, 0)),
        (Item("item6"), Placement(1, 0, 1)),
        (Item("item7"), Placement(1, 1, 0)),
        (Item("item8"), Placement(1, 1, 1)),
    ]

    storage_system_shape = StorageSystemShape("test_system", 2, 2, 2)
    storage_system = StorageSystem(
        shape=storage_system_shape,
    )
    for item, placement in items_and_placements:
        storage_system.items[placement].append(item)

    strategy = VerticalPlacementStrategy()
    candidate_placements = strategy(storage_system)

    assert len(candidate_placements) == 0
