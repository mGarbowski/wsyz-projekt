from dataclasses import dataclass, field
import enum


class Vegetable(enum.Enum):
    """Class representing the types of vegetables."""

    POTATO = enum.auto()
    CABBAGE = enum.auto()
    BEETROOT = enum.auto()
    CARROT = enum.auto()


type Coordinate = tuple[float, float]
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

    def __str__(self) -> str:
        return self.address


@dataclass(frozen=True, unsafe_hash=True)
class Manufacturer(Location):
    """Class representing a manufacturer."""

    city: str
    capabilities: dict[Vegetable, Kilos] = field(hash=False)

    def __str__(self) -> str:
        return self.city


@dataclass(frozen=True)
class Warehouse(Location):
    """Class representing a warehouse."""

    city: str
    capacity: Kilos

    def __str__(self) -> str:
        return self.city
