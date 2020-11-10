# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = place_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, Any, TypeVar, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class GeoType(Enum):
    """Type of this object."""
    GEO_COORDINATES = "GeoCoordinates"
    GEO_SHAPE = "GeoShape"


class Geo:
    """The geo coordinates of the place.
    
    The geographic coordinates of an entity.
    
    The geographic shape of a place. A GeoShape can be described using several properties
    whose values are based on latitude/longitude pairs. Either whitespace or commas can be
    used to separate latitude and longitude; whitespace should be used when writing a list of
    several such points.
    """
    type: GeoType
    """The latitude of a location. For example 37.42242 (WGS 84)."""
    latitude: Optional[float]
    """The longitude of a location. For example -122.08585 (WGS 84)."""
    longitude: Optional[float]
    """A box is the area enclosed by the rectangle formed by two points. The first point is the
    lower corner, the second point is the upper corner. A box is expressed as two points
    separated by a space character.
    """
    box: Optional[str]

    def __init__(self, type: GeoType, latitude: Optional[float], longitude: Optional[float], box: Optional[str]) -> None:
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.box = box

    @staticmethod
    def from_dict(obj: Any) -> 'Geo':
        assert isinstance(obj, dict)
        type = GeoType(obj.get("@type"))
        latitude = from_union([from_float, from_none], obj.get("latitude"))
        longitude = from_union([from_float, from_none], obj.get("longitude"))
        box = from_union([from_str, from_none], obj.get("box"))
        return Geo(type, latitude, longitude, box)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(GeoType, self.type)
        result["latitude"] = from_union([to_float, from_none], self.latitude)
        result["longitude"] = from_union([to_float, from_none], self.longitude)
        result["box"] = from_union([from_str, from_none], self.box)
        return result


class PlaceType(Enum):
    """Type of this object."""
    PLACE = "Place"


class Place:
    """Entities that have a somewhat fixed, physical extension."""
    type: PlaceType
    geo: Geo

    def __init__(self, type: PlaceType, geo: Geo) -> None:
        self.type = type
        self.geo = geo

    @staticmethod
    def from_dict(obj: Any) -> 'Place':
        assert isinstance(obj, dict)
        type = PlaceType(obj.get("@type"))
        geo = Geo.from_dict(obj.get("geo"))
        return Place(type, geo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(PlaceType, self.type)
        result["geo"] = to_class(Geo, self.geo)
        return result


def place_from_dict(s: Any) -> Place:
    return Place.from_dict(s)


def place_to_dict(x: Place) -> Any:
    return to_class(Place, x)
