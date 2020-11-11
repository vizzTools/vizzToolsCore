# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = coverage_provider_from_dict(json.loads(json_string))

from typing import Optional, Any, TypeVar, Type, cast
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


class CoverageOptions:
    """Coverage provider data specific options."""
    data_encoding: Optional[str]

    def __init__(self, data_encoding: Optional[str]) -> None:
        self.data_encoding = data_encoding

    @staticmethod
    def from_dict(obj: Any) -> 'CoverageOptions':
        assert isinstance(obj, dict)
        data_encoding = from_union([from_str, from_none], obj.get("DATA_ENCODING"))
        return CoverageOptions(data_encoding)

    def to_dict(self) -> dict:
        result: dict = {}
        result["DATA_ENCODING"] = from_union([from_str, from_none], self.data_encoding)
        return result


class TypeEnum(Enum):
    """Provider definition type."""
    COVERAGE = "coverage"


class CoverageProvider:
    """A vizzToolsCore CoverageProvider definition object that describes the connection of the
    dataset data.
    
    rasterio CoverageProvider
    
    xarray CoverageProvider
    """
    data: str
    format: Format
    name: str
    options: CoverageOptions
    type: TypeEnum
    time_field: Optional[str]
    x_field: Optional[str]
    y_field: Optional[str]

    def __init__(self, data: str, format: Format, name: str, options: CoverageOptions, type: TypeEnum, time_field: Optional[str], x_field: Optional[str], y_field: Optional[str]) -> None:
        self.data = data
        self.format = format
        self.name = name
        self.options = options
        self.type = type
        self.time_field = time_field
        self.x_field = x_field
        self.y_field = y_field

    @staticmethod
    def from_dict(obj: Any) -> 'CoverageProvider':
        assert isinstance(obj, dict)
        data = from_str(obj.get("data"))
        format = Format.from_dict(obj.get("format"))
        name = from_str(obj.get("name"))
        options = CoverageOptions.from_dict(obj.get("options"))
        type = TypeEnum(obj.get("type"))
        time_field = from_union([from_str, from_none], obj.get("time_field"))
        x_field = from_union([from_str, from_none], obj.get("x_field"))
        y_field = from_union([from_str, from_none], obj.get("y_field"))
        return CoverageProvider(data, format, name, options, type, time_field, x_field, y_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_str(self.data)
        result["format"] = to_class(Format, self.format)
        result["name"] = from_str(self.name)
        result["options"] = to_class(CoverageOptions, self.options)
        result["type"] = to_enum(TypeEnum, self.type)
        result["time_field"] = from_union([from_str, from_none], self.time_field)
        result["x_field"] = from_union([from_str, from_none], self.x_field)
        result["y_field"] = from_union([from_str, from_none], self.y_field)
        return result


def coverage_provider_from_dict(s: Any) -> CoverageProvider:
    return CoverageProvider.from_dict(s)


def coverage_provider_to_dict(x: CoverageProvider) -> Any:
    return to_class(CoverageProvider, x)
