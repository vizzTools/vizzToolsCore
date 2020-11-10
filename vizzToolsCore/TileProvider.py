# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = tile_provider_from_dict(json.loads(json_string))

from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from enum import Enum


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class Format:
    """Provider data format."""
    mimetype: Optional[str]
    name: Optional[str]

    def __init__(self, mimetype: Optional[str], name: Optional[str]) -> None:
        self.mimetype = mimetype
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Format':
        assert isinstance(obj, dict)
        mimetype = from_union([from_str, from_none], obj.get("mimetype"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Format(mimetype, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["mimetype"] = from_union([from_str, from_none], self.mimetype)
        result["name"] = from_union([from_str, from_none], self.name)
        return result


class Zoom:
    """Minimum and maximum zoom levels."""
    max: Optional[int]
    min: Optional[int]

    def __init__(self, max: Optional[int], min: Optional[int]) -> None:
        self.max = max
        self.min = min

    @staticmethod
    def from_dict(obj: Any) -> 'Zoom':
        assert isinstance(obj, dict)
        max = from_union([from_int, from_none], obj.get("max"))
        min = from_union([from_int, from_none], obj.get("min"))
        return Zoom(max, min)

    def to_dict(self) -> dict:
        result: dict = {}
        result["max"] = from_union([from_int, from_none], self.max)
        result["min"] = from_union([from_int, from_none], self.min)
        return result


class TileOptions:
    """Tile provider data specific options."""
    metadata_format: Optional[str]
    schemes: Optional[List[str]]
    zoom: Optional[Zoom]

    def __init__(self, metadata_format: Optional[str], schemes: Optional[List[str]], zoom: Optional[Zoom]) -> None:
        self.metadata_format = metadata_format
        self.schemes = schemes
        self.zoom = zoom

    @staticmethod
    def from_dict(obj: Any) -> 'TileOptions':
        assert isinstance(obj, dict)
        metadata_format = from_union([from_str, from_none], obj.get("metadata_format"))
        schemes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("schemes"))
        zoom = from_union([Zoom.from_dict, from_none], obj.get("zoom"))
        return TileOptions(metadata_format, schemes, zoom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["metadata_format"] = from_union([from_str, from_none], self.metadata_format)
        result["schemes"] = from_union([lambda x: from_list(from_str, x), from_none], self.schemes)
        result["zoom"] = from_union([lambda x: to_class(Zoom, x), from_none], self.zoom)
        return result


class TypeEnum(Enum):
    """Provider definition type."""
    COVERAGE = "coverage"


class TileProvider:
    """A vizzToolsCore TileProvider definition object that describes the connection of the
    dataset data.
    
    MVT TileProvider
    """
    data: str
    format: Format
    name: str
    options: TileOptions
    type: TypeEnum

    def __init__(self, data: str, format: Format, name: str, options: TileOptions, type: TypeEnum) -> None:
        self.data = data
        self.format = format
        self.name = name
        self.options = options
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'TileProvider':
        assert isinstance(obj, dict)
        data = from_str(obj.get("data"))
        format = Format.from_dict(obj.get("format"))
        name = from_str(obj.get("name"))
        options = TileOptions.from_dict(obj.get("options"))
        type = TypeEnum(obj.get("type"))
        return TileProvider(data, format, name, options, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_str(self.data)
        result["format"] = to_class(Format, self.format)
        result["name"] = from_str(self.name)
        result["options"] = to_class(TileOptions, self.options)
        result["type"] = to_enum(TypeEnum, self.type)
        return result


def tile_provider_from_dict(s: Any) -> TileProvider:
    return TileProvider.from_dict(s)


def tile_provider_to_dict(x: TileProvider) -> Any:
    return to_class(TileProvider, x)
