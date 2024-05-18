from dataclasses import dataclass, field
from utils import Vegetable


type Coordinate = tuple[float, float]
type Tons = int
type Kilos = int


@dataclass(frozen=True)
class Location:
    coordinates: Coordinate


@dataclass(frozen=True)
class Shop(Location):
    address: str
    on_site_warehouse_capacity: Kilos


@dataclass(frozen=True, unsafe_hash=True)
class Manufacturer(Location):
    city: str
    capabilities: dict[Vegetable, Tons] = field(hash=False)


@dataclass(frozen=True)
class Warehouse(Location):
    city: str
    capacity: Tons
