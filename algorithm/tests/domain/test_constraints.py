import pytest

from algorithm.domain.constraints import (
    ConstraintContext,
    ConstraintStatus,
    apply_max_height_constraint,
    apply_max_item_weight_constraint,
)
from algorithm.domain.exceptions import ItemMissingDataError
from algorithm.domain.models import Item, Placement, StorageSystem, StorageSystemShape
from algorithm.domain.strategies import VerticalPlacementStrategy


# TODO(parradam): create lists of placements, map them to items with method
class TestMaxHeightConstraint:
    def test_finds_placements(self) -> None:
        storage_system_shape = StorageSystemShape("test_system", 1, 1, 1)
        storage_system = StorageSystem(
            shape=storage_system_shape,
        )

        strategy = VerticalPlacementStrategy()
        candidate_placements = strategy(storage_system)

        input_context = ConstraintContext(
            storage_system,
            candidate_placements,
            Item("item99"),
        )
        output_context = apply_max_height_constraint(
            context=input_context,
            max_height=2,
            status=ConstraintStatus.ENABLED,
        )

        expected_constrained_placements = [
            Placement(0, 0, 0),
        ]

        assert output_context.placements == expected_constrained_placements

    def test_eliminates_invalid_placements(self) -> None:
        storage_system_shape = StorageSystemShape("test_system", 1, 2, 3)
        storage_system = StorageSystem(
            shape=storage_system_shape,
        )

        items_placements = {
            "item1": Placement(0, 0, 0),
            "item2": Placement(0, 1, 0),
        }
        for item, placement in items_placements.items():
            storage_system.items[placement].append(Item(item))

        strategy = VerticalPlacementStrategy()
        candidate_placements = strategy(storage_system)

        input_context = ConstraintContext(
            storage_system,
            candidate_placements,
            Item("item99"),
        )
        output_context = apply_max_height_constraint(
            context=input_context,
            max_height=2,
            status=ConstraintStatus.ENABLED,
        )

        expected_constrained_placements = [
            Placement(0, 0, 1),
            Placement(0, 1, 1),
        ]

        assert output_context.placements == expected_constrained_placements

    def test_finds_no_placements(self) -> None:
        storage_system_shape = StorageSystemShape("test_system", 1, 1, 4)
        storage_system = StorageSystem(
            shape=storage_system_shape,
        )

        items_placements = {
            "item1": Placement(0, 0, 0),  # 1 -> single stack
        }
        for item, placement in items_placements.items():
            storage_system.items[placement].append(Item(item))

        strategy = VerticalPlacementStrategy()
        candidate_placements = strategy(storage_system)

        input_context = ConstraintContext(
            storage_system,
            candidate_placements,
            Item("item99"),
        )
        output_context = apply_max_height_constraint(
            context=input_context,
            max_height=1,
            status=ConstraintStatus.ENABLED,
        )

        assert len(output_context.placements) == 0

    def test_returns_empty_list_if_given_empty_list(self) -> None:
        storage_system_shape = StorageSystemShape("test_system", 2, 2, 2)
        storage_system = StorageSystem(
            shape=storage_system_shape,
        )

        candidate_placements: list[Placement] = []

        input_context = ConstraintContext(
            storage_system,
            candidate_placements,
            Item("item99"),
        )
        output_context = apply_max_height_constraint(
            context=input_context,
            max_height=1,
            status=ConstraintStatus.ENABLED,
        )

        assert len(output_context.placements) == 0


class TestMaxItemWeightConstraint:
    def test_finds_placements(self) -> None:
        storage_system_shape = StorageSystemShape("test_system", 1, 1, 1)
        storage_system = StorageSystem(
            shape=storage_system_shape,
            max_weight=5,
        )

        strategy = VerticalPlacementStrategy()
        candidate_placements = strategy(storage_system)

        input_context = ConstraintContext(
            storage_system,
            candidate_placements,
            Item("item99", weight=3),
        )
        output_context = apply_max_item_weight_constraint(
            context=input_context,
            status=ConstraintStatus.ENABLED,
        )

        expected_constrained_placements = [
            Placement(0, 0, 0),
        ]

        assert output_context.placements == expected_constrained_placements

    def test_finds_no_placements(self) -> None:
        storage_system_shape = StorageSystemShape("test_system", 1, 1, 1)
        storage_system = StorageSystem(
            shape=storage_system_shape,
            max_weight=1,
        )

        strategy = VerticalPlacementStrategy()
        candidate_placements = strategy(storage_system)

        input_context = ConstraintContext(
            storage_system,
            candidate_placements,
            Item("item99", weight=3),
        )
        output_context = apply_max_item_weight_constraint(
            context=input_context,
            status=ConstraintStatus.ENABLED,
        )

        assert len(output_context.placements) == 0

    def test_raises_domain_error_if_weights_missing(
        self,
    ) -> None:
        storage_system_shape = StorageSystemShape("test_system", 1, 1, 1)
        storage_system = StorageSystem(
            shape=storage_system_shape,
        )

        strategy = VerticalPlacementStrategy()
        candidate_placements = strategy(storage_system)

        input_context = ConstraintContext(
            storage_system,
            candidate_placements,
            Item("item99", weight=3),
        )

        with pytest.raises(ItemMissingDataError):
            apply_max_item_weight_constraint(
                context=input_context,
                status=ConstraintStatus.ENABLED,
            )
