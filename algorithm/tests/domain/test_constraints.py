import pytest

from algorithm.domain.constraints import MaxHeightConstraint, MaxItemWeightConstraint
from algorithm.domain.exceptions import ItemMissingDataError
from algorithm.domain.models import Item, Placement, StorageSystem, StorageSystemShape
from algorithm.domain.strategies import VerticalPlacementStrategy


# TODO(parradam): create lists of placements, map them to items with method
class TestMaxHeightConstraint:
    def test_finds_placements(self) -> None:
        items_placements = {
            "item1": Placement(0, 1, 0),  # 1 -> single stack
            "item2": Placement(1, 0, 0),  # 2, 3 -> double stack
            "item3": Placement(1, 0, 1),
            "item4": Placement(1, 1, 0),  # 4, 5, 6 -> triple stack
            "item5": Placement(1, 1, 1),
            "item6": Placement(1, 1, 2),
        }

        storage_system_shape = StorageSystemShape("test_system", 2, 2, 4)
        storage_system = StorageSystem(
            shape=storage_system_shape,
        )
        for item, placement in items_placements.items():
            storage_system.items[placement].append(Item(item))

        strategy = VerticalPlacementStrategy()
        candidate_placements = strategy(storage_system)

        # apply the max height constraint
        max_height_constraint = MaxHeightConstraint(max_height=3)
        constrained_placements = max_height_constraint.apply(
            storage_system,
            candidate_placements,
            Item("item99"),
        )

        expected_constrained_placements = [
            Placement(0, 0, 0),
            Placement(0, 1, 1),
            Placement(1, 0, 2),
        ]

        assert constrained_placements == expected_constrained_placements

    def test_finds_no_placements(self) -> None:
        items_placements = {
            "item1": Placement(0, 0, 0),  # 1 -> single stack
        }

        storage_system_shape = StorageSystemShape("test_system", 1, 1, 1)
        storage_system = StorageSystem(
            shape=storage_system_shape,
        )
        for item, placement in items_placements.items():
            storage_system.items[placement].append(Item(item))

        strategy = VerticalPlacementStrategy()
        candidate_placements = strategy(storage_system)

        # apply the max height constraint
        max_height_constraint = MaxHeightConstraint(max_height=3)
        constrained_placements = max_height_constraint.apply(
            storage_system,
            candidate_placements,
            Item("item99"),
        )

        assert len(constrained_placements) == 0

    def test_returns_empty_list_if_given_empty_list(self) -> None:
        storage_system_shape = StorageSystemShape("test_system", 2, 2, 2)
        storage_system = StorageSystem(
            shape=storage_system_shape,
        )

        candidate_placements: list[Placement] = []

        # apply the max height constraint
        max_height_constraint = MaxHeightConstraint(max_height=3)
        constrained_placements = max_height_constraint.apply(
            storage_system,
            candidate_placements,
            Item("item99"),
        )

        assert len(constrained_placements) == 0


class TestMaxItemWeightConstraint:
    def test_finds_placements(self) -> None:
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
            storage_system,
            candidate_placements,
            Item("item99", weight=3),
        )

        expected_constrained_placements = [
            Placement(0, 0, 0),
        ]

        assert constrained_placements == expected_constrained_placements

    def test_finds_no_placements(self) -> None:
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
            storage_system,
            candidate_placements,
            Item("item99", weight=3),
        )

        assert len(constrained_placements) == 0

    def test_raises_domain_error_if_weights_missing(
        self,
    ) -> None:
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
                storage_system,
                candidate_placements,
                Item("item99"),
            )
