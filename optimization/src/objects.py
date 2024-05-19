from dataclasses import dataclass, field
import enum


class Vegetable(enum.Enum):
    """Class representing the types of vegetables."""

    POTATO = enum.auto()
    CABBAGE = enum.auto()
    BEETROOT = enum.auto()
    CARROT = enum.auto()


type Coordinate = tuple[float, float]
type Tons = int
type Kilos = int


@dataclass(frozen=True)
class Location:
    """Base class for all locations."""

    coordinates: Coordinate


@dataclass(frozen=True)
class Shop(Location):
    """Class representing a shop."""

    address: str
    on_site_warehouse_capacity: Kilos


@dataclass(frozen=True, unsafe_hash=True)
class Manufacturer(Location):
    """Class representing a manufacturer."""

    city: str
    capabilities: dict[Vegetable, Tons] = field(hash=False)


@dataclass(frozen=True)
class Warehouse(Location):
    """Class representing a warehouse."""

    city: str
    capacity: Tons
