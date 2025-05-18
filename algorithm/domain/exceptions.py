class StorageSystemError(Exception):
    """Base class for all exceptions related to the storage system."""

    pass


class StrategyError(Exception):
    """Base class for all exceptions related to placement strategies."""

    pass


class ConstraintError(Exception):
    """Base class for all exceptions related to constraints."""

    pass


class PlacementError(Exception):
    """Base class for all exceptions related to placements."""

    pass
