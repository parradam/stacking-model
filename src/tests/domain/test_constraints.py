import pytest

from src.domain.constraints import (
    ConstraintStatus,
    apply_max_height_constraint,
    apply_max_item_weight_constraint,
)
from src.domain.context import PutawayContext
from src.domain.item import Item, ItemMissingDataError
from src.domain.placement import Placement
from src.domain.storage_system import (
    StorageSystem,
    StorageSystemShape,
)


# TODO(parradam): create lists of placements, map them to items with method
class TestMaxHeightConstraint:
    def test_finds_placements(self) -> None:
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 1, 1, 1),
        )
        placements = [
            Placement(0, 0, 0),
        ]
        item = Item("item99")

        input_context = PutawayContext(
            system=system,
            placements=placements,
            item=item,
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
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 1, 2, 3),
        )
        placements = [
            Placement(0, 0, 0),
            Placement(0, 1, 0),
            Placement(0, 0, 1),
            Placement(0, 1, 1),
            Placement(0, 0, 2),
            Placement(0, 1, 2),
        ]
        item = Item("item99")

        input_context = PutawayContext(
            system=system,
            placements=placements,
            item=item,
        )
        output_context = apply_max_height_constraint(
            context=input_context,
            max_height=2,
            status=ConstraintStatus.ENABLED,
        )

        expected_constrained_placements = [
            Placement(0, 0, 0),
            Placement(0, 1, 0),
            Placement(0, 0, 1),
            Placement(0, 1, 1),
        ]

        assert output_context.placements == expected_constrained_placements

    def test_finds_no_placements(self) -> None:
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 1, 1, 4),
        )
        placements = [
            Placement(0, 0, 0),
            Placement(0, 0, 1),
            Placement(0, 0, 2),
            Placement(0, 0, 3),
        ]
        item = Item("item99")

        input_context = PutawayContext(
            system=system,
            placements=placements,
            item=item,
        )
        output_context = apply_max_height_constraint(
            context=input_context,
            max_height=0,
            status=ConstraintStatus.ENABLED,
        )

        assert len(output_context.placements) == 0

    def test_returns_empty_list_if_given_empty_list(self) -> None:
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 2, 2, 2),
        )
        placements: list[Placement] = []

        input_context = PutawayContext(
            system=system,
            placements=placements,
            item=Item("item99"),
        )
        output_context = apply_max_height_constraint(
            context=input_context,
            max_height=1,
            status=ConstraintStatus.ENABLED,
        )

        assert len(output_context.placements) == 0


class TestMaxItemWeightConstraint:
    def test_finds_placements(self) -> None:
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 1, 1, 1),
            max_weight=5,
        )
        placements = [
            Placement(0, 0, 0),
        ]
        item = Item("item99", weight=3)

        input_context = PutawayContext(
            system=system,
            placements=placements,
            item=item,
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
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 1, 1, 1),
            max_weight=1,
        )
        placements = [
            Placement(0, 0, 0),
        ]
        item = Item("item99", weight=3)

        input_context = PutawayContext(
            system=system,
            placements=placements,
            item=item,
        )
        output_context = apply_max_item_weight_constraint(
            context=input_context,
            status=ConstraintStatus.ENABLED,
        )

        assert len(output_context.placements) == 0

    def test_raises_domain_error_if_weights_missing(
        self,
    ) -> None:
        system = StorageSystem(
            shape=StorageSystemShape("test_system", 1, 1, 1),
        )
        placements = [
            Placement(0, 0, 0),
        ]
        item = Item("item99", weight=3)

        input_context = PutawayContext(
            system=system,
            placements=placements,
            item=item,
        )

        with pytest.raises(ItemMissingDataError):
            apply_max_item_weight_constraint(
                context=input_context,
                status=ConstraintStatus.ENABLED,
            )
