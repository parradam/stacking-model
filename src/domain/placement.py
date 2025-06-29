from dataclasses import dataclass


class PlacementError(Exception):
    """Base class for all exceptions related to placements."""


@dataclass(frozen=True)
class Placement:
    x: int
    y: int
    z: int
