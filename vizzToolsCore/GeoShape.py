# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = geo_shape_from_dict(json.loads(json_string))

from enum import Enum
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class TypeEnum(Enum):
    """Type of this object."""
    GEO_SHAPE = "GeoShape"


class GeoShape:
    """The geographic shape of a place. A GeoShape can be described using several properties
    whose values are based on latitude/longitude pairs. Either whitespace or commas can be
    used to separate latitude and longitude; whitespace should be used when writing a list of
    several such points.
    """
    type: TypeEnum
    """A box is the area enclosed by the rectangle formed by two points. The first point is the
    lower corner, the second point is the upper corner. A box is expressed as two points
    separated by a space character.
    """
    box: str

    def __init__(self, type: TypeEnum, box: str) -> None:
        self.type = type
        self.box = box

    @staticmethod
    def from_dict(obj: Any) -> 'GeoShape':
        assert isinstance(obj, dict)
        type = TypeEnum(obj.get("@type"))
        box = from_str(obj.get("box"))
        return GeoShape(type, box)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(TypeEnum, self.type)
        result["box"] = from_str(self.box)
        return result


def geo_shape_from_dict(s: Any) -> GeoShape:
    return GeoShape.from_dict(s)


def geo_shape_to_dict(x: GeoShape) -> Any:
    return to_class(GeoShape, x)
