import pytest
from algorithm.domain.models import Placement, Item, StorageSystemShape, StorageSystem
from algorithm.domain.strategies import VerticalPlacementStrategy
from algorithm.domain.constraints import MaxHeightConstraint, MaxItemWeightConstraint
from algorithm.domain.exceptions import ItemMissingDataError


def test_max_height_constraint_finds_placements():
    items_and_placements = [
        (Item("item1"), Placement(0, 1, 0)),  # 1 -> single stack
        (Item("item2"), Placement(1, 0, 0)),  # 2, 3 -> double stack
        (Item("item3"), Placement(1, 0, 1)),  #
        (Item("item4"), Placement(1, 1, 0)),  # 4, 5, 6 -> triple stack
        (Item("item5"), Placement(1, 1, 1)),  #
        (Item("item6"), Placement(1, 1, 2)),  #
    ]

    storage_system_shape = StorageSystemShape("test_system", 2, 2, 4)
    storage_system = StorageSystem(
        shape=storage_system_shape,
    )
    for item, placement in items_and_placements:
        storage_system.items[placement].append(item)

    strategy = VerticalPlacementStrategy()
    candidate_placements = strategy(storage_system)

    # apply the max height constraint
    max_height_constraint = MaxHeightConstraint(max_height=3)
    constrained_placements = max_height_constraint.apply(
        storage_system, candidate_placements, Item("item99")
    )

    expected_constrained_placements = [
        Placement(0, 0, 0),
        Placement(0, 1, 1),
        Placement(1, 0, 2),
    ]

    assert constrained_placements == expected_constrained_placements


def test_max_height_constraint_finds_no_placements():
    items_and_placements = [
        (Item("item1"), Placement(0, 0, 0)),  # 1 -> single stack
    ]

    storage_system_shape = StorageSystemShape("test_system", 1, 1, 1)
    storage_system = StorageSystem(
        shape=storage_system_shape,
    )
    for item, placement in items_and_placements:
        storage_system.items[placement].append(item)

    strategy = VerticalPlacementStrategy()
    candidate_placements = strategy(storage_system)

    # apply the max height constraint
    max_height_constraint = MaxHeightConstraint(max_height=3)
    constrained_placements = max_height_constraint.apply(
        storage_system, candidate_placements, Item("item99")
    )

    assert len(constrained_placements) == 0


def test_max_height_constraint_returns_empty_list_if_given_empty_list():
    storage_system_shape = StorageSystemShape("test_system", 2, 2, 2)
    storage_system = StorageSystem(
        shape=storage_system_shape,
    )

    candidate_placements: list[Placement] = []

    # apply the max height constraint
    max_height_constraint = MaxHeightConstraint(max_height=3)
    constrained_placements = max_height_constraint.apply(
        storage_system, candidate_placements, Item("item99")
    )

    assert len(constrained_placements) == 0


def test_max_item_weight_constraint_finds_placements():
    storage_system_shape = StorageSystemShape("test_system", 1, 1, 1)
    storage_system = StorageSystem(
        shape=storage_system_shape,
        max_weight=5,
    )

    strategy = VerticalPlacementStrategy()
    candidate_placements = strategy(storage_system)

    # apply the max weight constraint
    max_item_weight_constraint = MaxItemWeightConstraint()
    constrained_placements = max_item_weight_constraint.apply(
        storage_system, candidate_placements, Item("item99", weight=3)
    )

    expected_constrained_placements = [
        Placement(0, 0, 0),
    ]

    assert constrained_placements == expected_constrained_placements


def test_max_item_weight_constraint_finds_no_placements():
    storage_system_shape = StorageSystemShape("test_system", 1, 1, 1)
    storage_system = StorageSystem(
        shape=storage_system_shape,
        max_weight=1,
    )

    strategy = VerticalPlacementStrategy()
    candidate_placements = strategy(storage_system)

    # apply the max weight constraint
    max_item_weight_constraint = MaxItemWeightConstraint()
    constrained_placements = max_item_weight_constraint.apply(
        storage_system, candidate_placements, Item("item99", weight=3)
    )

    assert len(constrained_placements) == 0


def test_max_item_weight_constraint_raises_domain_error_if_weights_missing():
    storage_system_shape = StorageSystemShape("test_system", 1, 1, 1)
    storage_system = StorageSystem(
        shape=storage_system_shape,
    )

    strategy = VerticalPlacementStrategy()
    candidate_placements = strategy(storage_system)

    # apply the max weight constraint
    max_item_weight_constraint = MaxItemWeightConstraint()

    with pytest.raises(ItemMissingDataError):
        max_item_weight_constraint.apply(
            storage_system, candidate_placements, Item("item99")
        )
