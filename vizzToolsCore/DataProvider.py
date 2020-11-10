# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = data_provider_from_dict(json.loads(json_string))

from typing import Optional, List, Any, Union, TypeVar, Callable, Type, cast
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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


class DatabaseData:
    """Object defining database connection."""
    dbname: Optional[str]
    host: Optional[str]
    password: Optional[str]
    search_path: Optional[List[str]]
    user: Optional[str]

    def __init__(self, dbname: Optional[str], host: Optional[str], password: Optional[str], search_path: Optional[List[str]], user: Optional[str]) -> None:
        self.dbname = dbname
        self.host = host
        self.password = password
        self.search_path = search_path
        self.user = user

    @staticmethod
    def from_dict(obj: Any) -> 'DatabaseData':
        assert isinstance(obj, dict)
        dbname = from_union([from_str, from_none], obj.get("dbname"))
        host = from_union([from_str, from_none], obj.get("host"))
        password = from_union([from_str, from_none], obj.get("password"))
        search_path = from_union([lambda x: from_list(from_str, x), from_none], obj.get("search_path"))
        user = from_union([from_str, from_none], obj.get("user"))
        return DatabaseData(dbname, host, password, search_path, user)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dbname"] = from_union([from_str, from_none], self.dbname)
        result["host"] = from_union([from_str, from_none], self.host)
        result["password"] = from_union([from_str, from_none], self.password)
        result["search_path"] = from_union([lambda x: from_list(from_str, x), from_none], self.search_path)
        result["user"] = from_union([from_str, from_none], self.user)
        return result


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


class Options:
    """Provider data specific options.
    
    Coverage provider data specific options.
    
    Tile provider data specific options.
    """
    data_encoding: Optional[str]
    metadata_format: Optional[str]
    schemes: Optional[List[str]]
    zoom: Optional[Zoom]

    def __init__(self, data_encoding: Optional[str], metadata_format: Optional[str], schemes: Optional[List[str]], zoom: Optional[Zoom]) -> None:
        self.data_encoding = data_encoding
        self.metadata_format = metadata_format
        self.schemes = schemes
        self.zoom = zoom

    @staticmethod
    def from_dict(obj: Any) -> 'Options':
        assert isinstance(obj, dict)
        data_encoding = from_union([from_str, from_none], obj.get("DATA_ENCODING"))
        metadata_format = from_union([from_str, from_none], obj.get("metadata_format"))
        schemes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("schemes"))
        zoom = from_union([Zoom.from_dict, from_none], obj.get("zoom"))
        return Options(data_encoding, metadata_format, schemes, zoom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["DATA_ENCODING"] = from_union([from_str, from_none], self.data_encoding)
        result["metadata_format"] = from_union([from_str, from_none], self.metadata_format)
        result["schemes"] = from_union([lambda x: from_list(from_str, x), from_none], self.schemes)
        result["zoom"] = from_union([lambda x: to_class(Zoom, x), from_none], self.zoom)
        return result


class TypeEnum(Enum):
    """Provider definition type."""
    COVERAGE = "coverage"


class DataProviderClass:
    data: Union[DatabaseData, str]
    format: Optional[Format]
    geom_field: Optional[str]
    id_field: Optional[str]
    name: str
    options: Optional[Options]
    table: Optional[str]
    time_field: Optional[str]
    type: TypeEnum
    x_field: Optional[str]
    y_field: Optional[str]

    def __init__(self, data: Union[DatabaseData, str], format: Optional[Format], geom_field: Optional[str], id_field: Optional[str], name: str, options: Optional[Options], table: Optional[str], time_field: Optional[str], type: TypeEnum, x_field: Optional[str], y_field: Optional[str]) -> None:
        self.data = data
        self.format = format
        self.geom_field = geom_field
        self.id_field = id_field
        self.name = name
        self.options = options
        self.table = table
        self.time_field = time_field
        self.type = type
        self.x_field = x_field
        self.y_field = y_field

    @staticmethod
    def from_dict(obj: Any) -> 'DataProviderClass':
        assert isinstance(obj, dict)
        data = from_union([DatabaseData.from_dict, from_str], obj.get("data"))
        format = from_union([Format.from_dict, from_none], obj.get("format"))
        geom_field = from_union([from_str, from_none], obj.get("geom_field"))
        id_field = from_union([from_str, from_none], obj.get("id_field"))
        name = from_str(obj.get("name"))
        options = from_union([Options.from_dict, from_none], obj.get("options"))
        table = from_union([from_str, from_none], obj.get("table"))
        time_field = from_union([from_str, from_none], obj.get("time_field"))
        type = TypeEnum(obj.get("type"))
        x_field = from_union([from_str, from_none], obj.get("x_field"))
        y_field = from_union([from_str, from_none], obj.get("y_field"))
        return DataProviderClass(data, format, geom_field, id_field, name, options, table, time_field, type, x_field, y_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: to_class(DatabaseData, x), from_str], self.data)
        result["format"] = from_union([lambda x: to_class(Format, x), from_none], self.format)
        result["geom_field"] = from_union([from_str, from_none], self.geom_field)
        result["id_field"] = from_union([from_str, from_none], self.id_field)
        result["name"] = from_str(self.name)
        result["options"] = from_union([lambda x: to_class(Options, x), from_none], self.options)
        result["table"] = from_union([from_str, from_none], self.table)
        result["time_field"] = from_union([from_str, from_none], self.time_field)
        result["type"] = to_enum(TypeEnum, self.type)
        result["x_field"] = from_union([from_str, from_none], self.x_field)
        result["y_field"] = from_union([from_str, from_none], self.y_field)
        return result


def data_provider_from_dict(s: Any) -> Union[List[Any], bool, DataProviderClass, float, int, None, str]:
    return from_union([from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), DataProviderClass.from_dict], s)


def data_provider_to_dict(x: Union[List[Any], bool, DataProviderClass, float, int, None, str]) -> Any:
    return from_union([from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), lambda x: to_class(DataProviderClass, x)], x)
