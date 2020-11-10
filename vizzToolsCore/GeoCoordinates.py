# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = geo_coordinates_from_dict(json.loads(json_string))

from enum import Enum
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class TypeEnum(Enum):
    """Type of this object."""
    GEO_COORDINATES = "GeoCoordinates"


class GeoCoordinates:
    """The geographic coordinates of an entity."""
    type: TypeEnum
    """The latitude of a location. For example 37.42242 (WGS 84)."""
    latitude: float
    """The longitude of a location. For example -122.08585 (WGS 84)."""
    longitude: float

    def __init__(self, type: TypeEnum, latitude: float, longitude: float) -> None:
        self.type = type
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def from_dict(obj: Any) -> 'GeoCoordinates':
        assert isinstance(obj, dict)
        type = TypeEnum(obj.get("@type"))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        return GeoCoordinates(type, latitude, longitude)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(TypeEnum, self.type)
        result["latitude"] = to_float(self.latitude)
        result["longitude"] = to_float(self.longitude)
        return result


def geo_coordinates_from_dict(s: Any) -> GeoCoordinates:
    return GeoCoordinates.from_dict(s)


def geo_coordinates_to_dict(x: GeoCoordinates) -> Any:
    return to_class(GeoCoordinates, x)
