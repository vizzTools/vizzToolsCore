# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = feature_provider_from_dict(json.loads(json_string))

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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


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


class TypeEnum(Enum):
    """Provider definition type."""
    COVERAGE = "coverage"


class FeatureProvider:
    """A vizzToolsCore FeatureProvider definition object that describes the connection of the
    dataset data.
    
    CSV featureProvider
    
    GeoJSON FeatureProvider
    
    Elasticsearch FeatureProvider
    
    SQLiteGPKG featureProvider
    
    PostgreSQL featureProvider
    """
    data: Union[DatabaseData, str]
    id_field: str
    name: str
    type: TypeEnum
    time_field: Optional[str]
    table: Optional[str]
    geom_field: Optional[str]

    def __init__(self, data: Union[DatabaseData, str], id_field: str, name: str, type: TypeEnum, time_field: Optional[str], table: Optional[str], geom_field: Optional[str]) -> None:
        self.data = data
        self.id_field = id_field
        self.name = name
        self.type = type
        self.time_field = time_field
        self.table = table
        self.geom_field = geom_field

    @staticmethod
    def from_dict(obj: Any) -> 'FeatureProvider':
        assert isinstance(obj, dict)
        data = from_union([from_str, DatabaseData.from_dict], obj.get("data"))
        id_field = from_str(obj.get("id_field"))
        name = from_str(obj.get("name"))
        type = TypeEnum(obj.get("type"))
        time_field = from_union([from_str, from_none], obj.get("time_field"))
        table = from_union([from_str, from_none], obj.get("table"))
        geom_field = from_union([from_str, from_none], obj.get("geom_field"))
        return FeatureProvider(data, id_field, name, type, time_field, table, geom_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([from_str, lambda x: to_class(DatabaseData, x)], self.data)
        result["id_field"] = from_str(self.id_field)
        result["name"] = from_str(self.name)
        result["type"] = to_enum(TypeEnum, self.type)
        result["time_field"] = from_union([from_str, from_none], self.time_field)
        result["table"] = from_union([from_str, from_none], self.table)
        result["geom_field"] = from_union([from_str, from_none], self.geom_field)
        return result


def feature_provider_from_dict(s: Any) -> FeatureProvider:
    return FeatureProvider.from_dict(s)


def feature_provider_to_dict(x: FeatureProvider) -> Any:
    return to_class(FeatureProvider, x)
