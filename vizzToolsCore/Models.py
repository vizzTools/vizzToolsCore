# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = coverage_provider_from_dict(json.loads(json_string))
#     result = feature_provider_from_dict(json.loads(json_string))
#     result = tile_provider_from_dict(json.loads(json_string))
#     result = dataset_from_dict(json.loads(json_string))
#     result = organization_from_dict(json.loads(json_string))
#     result = person_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, Union, Dict, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Format:
    """Provider data format."""
    mimetype: Optional[str]
    name: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Format':
        assert isinstance(obj, dict)
        mimetype = from_union([from_none, from_str], obj.get("mimetype"))
        name = from_union([from_none, from_str], obj.get("name"))
        return Format(mimetype, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["mimetype"] = from_union([from_none, from_str], self.mimetype)
        result["name"] = from_union([from_none, from_str], self.name)
        return result


class CoverageProviderName(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    RASTERIO = "rasterio"
    XARRAY = "xarray"


@dataclass
class CoverageOptions:
    """Coverage provider data specific options."""
    data_encoding: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'CoverageOptions':
        assert isinstance(obj, dict)
        data_encoding = from_union([from_none, from_str], obj.get("DATA_ENCODING"))
        return CoverageOptions(data_encoding)

    def to_dict(self) -> dict:
        result: dict = {}
        result["DATA_ENCODING"] = from_union([from_none, from_str], self.data_encoding)
        return result


class CoverageProviderType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    COVERAGE = "coverage"


@dataclass
class CoverageProvider:
    """A vizzToolsCore CoverageProvider definition object that describes the connection of the
    dataset data.
    
    rasterio CoverageProvider
    
    xarray CoverageProvider
    """
    data: str
    format: Format
    name: CoverageProviderName
    options: CoverageOptions
    type: CoverageProviderType
    time_field: Optional[str]
    x_field: Optional[str]
    y_field: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'CoverageProvider':
        assert isinstance(obj, dict)
        data = from_str(obj.get("data"))
        format = Format.from_dict(obj.get("format"))
        name = CoverageProviderName(obj.get("name"))
        options = CoverageOptions.from_dict(obj.get("options"))
        type = CoverageProviderType(obj.get("type"))
        time_field = from_union([from_none, from_str], obj.get("time_field"))
        x_field = from_union([from_none, from_str], obj.get("x_field"))
        y_field = from_union([from_none, from_str], obj.get("y_field"))
        return CoverageProvider(data, format, name, options, type, time_field, x_field, y_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_str(self.data)
        result["format"] = to_class(Format, self.format)
        result["name"] = to_enum(CoverageProviderName, self.name)
        result["options"] = to_class(CoverageOptions, self.options)
        result["type"] = to_enum(CoverageProviderType, self.type)
        result["time_field"] = from_union([from_none, from_str], self.time_field)
        result["x_field"] = from_union([from_none, from_str], self.x_field)
        result["y_field"] = from_union([from_none, from_str], self.y_field)
        return result


@dataclass
class DatabaseData:
    """Object defining database connection."""
    dbname: Optional[str]
    host: Optional[str]
    password: Optional[str]
    search_path: Optional[List[str]]
    user: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'DatabaseData':
        assert isinstance(obj, dict)
        dbname = from_union([from_none, from_str], obj.get("dbname"))
        host = from_union([from_none, from_str], obj.get("host"))
        password = from_union([from_none, from_str], obj.get("password"))
        search_path = from_union([lambda x: from_list(from_str, x), from_none], obj.get("search_path"))
        user = from_union([from_none, from_str], obj.get("user"))
        return DatabaseData(dbname, host, password, search_path, user)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dbname"] = from_union([from_none, from_str], self.dbname)
        result["host"] = from_union([from_none, from_str], self.host)
        result["password"] = from_union([from_none, from_str], self.password)
        result["search_path"] = from_union([lambda x: from_list(from_str, x), from_none], self.search_path)
        result["user"] = from_union([from_none, from_str], self.user)
        return result


class FeatureProviderName(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    CSV = "CSV"
    ELASTICSEARCH = "Elasticsearch"
    GEO_JSON = "GeoJSON"
    POSTGRE_SQL = "PostgreSQL"
    SQ_LITE_GPKG = "SQLiteGPKG"


class FeatureProviderType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    FEATURE = "feature"


@dataclass
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
    name: FeatureProviderName
    type: FeatureProviderType
    geom_field: Optional[str]
    table: Optional[str]
    time_field: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'FeatureProvider':
        assert isinstance(obj, dict)
        data = from_union([DatabaseData.from_dict, from_str], obj.get("data"))
        id_field = from_str(obj.get("id_field"))
        name = FeatureProviderName(obj.get("name"))
        type = FeatureProviderType(obj.get("type"))
        geom_field = from_union([from_none, from_str], obj.get("geom_field"))
        table = from_union([from_none, from_str], obj.get("table"))
        time_field = from_union([from_none, from_str], obj.get("time_field"))
        return FeatureProvider(data, id_field, name, type, geom_field, table, time_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: to_class(DatabaseData, x), from_str], self.data)
        result["id_field"] = from_str(self.id_field)
        result["name"] = to_enum(FeatureProviderName, self.name)
        result["type"] = to_enum(FeatureProviderType, self.type)
        result["geom_field"] = from_union([from_none, from_str], self.geom_field)
        result["table"] = from_union([from_none, from_str], self.table)
        result["time_field"] = from_union([from_none, from_str], self.time_field)
        return result


class TileProviderName(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    MVT = "MVT"


@dataclass
class Zoom:
    """Minimum and maximum zoom levels."""
    max: Optional[int]
    min: Optional[int]

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


@dataclass
class TileOptions:
    """Tile provider data specific options."""
    metadata_format: Optional[str]
    schemes: Optional[List[str]]
    zoom: Optional[Zoom]

    @staticmethod
    def from_dict(obj: Any) -> 'TileOptions':
        assert isinstance(obj, dict)
        metadata_format = from_union([from_none, from_str], obj.get("metadata_format"))
        schemes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("schemes"))
        zoom = from_union([Zoom.from_dict, from_none], obj.get("zoom"))
        return TileOptions(metadata_format, schemes, zoom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["metadata_format"] = from_union([from_none, from_str], self.metadata_format)
        result["schemes"] = from_union([lambda x: from_list(from_str, x), from_none], self.schemes)
        result["zoom"] = from_union([lambda x: to_class(Zoom, x), from_none], self.zoom)
        return result


class TileProviderType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    TILE = "tile"


@dataclass
class TileProvider:
    """A vizzToolsCore TileProvider definition object that describes the connection of the
    dataset data.
    
    MVT TileProvider
    """
    data: str
    format: Format
    name: TileProviderName
    options: TileOptions
    type: TileProviderType

    @staticmethod
    def from_dict(obj: Any) -> 'TileProvider':
        assert isinstance(obj, dict)
        data = from_str(obj.get("data"))
        format = Format.from_dict(obj.get("format"))
        name = TileProviderName(obj.get("name"))
        options = TileOptions.from_dict(obj.get("options"))
        type = TileProviderType(obj.get("type"))
        return TileProvider(data, format, name, options, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_str(self.data)
        result["format"] = to_class(Format, self.format)
        result["name"] = to_enum(TileProviderName, self.name)
        result["options"] = to_class(TileOptions, self.options)
        result["type"] = to_enum(TileProviderType, self.type)
        return result


class ContactPointType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    CONTACT_POINT = "ContactPoint"


@dataclass
class ContactPoint:
    """A contact point—for example, a Customer Complaints department."""
    type: ContactPointType
    email: str
    contact_type: Optional[str]
    telephone: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'ContactPoint':
        assert isinstance(obj, dict)
        type = ContactPointType(obj.get("@type"))
        email = from_str(obj.get("email"))
        contact_type = from_union([from_none, from_str], obj.get("contactType"))
        telephone = from_union([from_none, from_str], obj.get("telephone"))
        return ContactPoint(type, email, contact_type, telephone)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(ContactPointType, self.type)
        result["email"] = from_str(self.email)
        result["contactType"] = from_union([from_none, from_str], self.contact_type)
        result["telephone"] = from_union([from_none, from_str], self.telephone)
        return result


class OrganizationType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    ORGANIZATION = "Organization"


@dataclass
class OrganizationClass:
    """An organization such as a school, NGO, corporation, club, etc."""
    type: OrganizationType
    name: str
    id: Optional[str]
    contact_point: Optional[ContactPoint]
    same_as: Optional[str]
    url: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'OrganizationClass':
        assert isinstance(obj, dict)
        type = OrganizationType(obj.get("@type"))
        name = from_str(obj.get("name"))
        id = from_union([from_none, from_str], obj.get("@id"))
        contact_point = from_union([ContactPoint.from_dict, from_none], obj.get("contactPoint"))
        same_as = from_union([from_none, from_str], obj.get("sameAs"))
        url = from_union([from_none, from_str], obj.get("url"))
        return OrganizationClass(type, name, id, contact_point, same_as, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(OrganizationType, self.type)
        result["name"] = from_str(self.name)
        result["@id"] = from_union([from_none, from_str], self.id)
        result["contactPoint"] = from_union([lambda x: to_class(ContactPoint, x), from_none], self.contact_point)
        result["sameAs"] = from_union([from_none, from_str], self.same_as)
        result["url"] = from_union([from_none, from_str], self.url)
        return result


class PersonOrganizationType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    ORGANIZATION = "Organization"
    PERSON = "Person"


@dataclass
class PersonOrganization:
    """An array of schema.org Person or Organization objects. To uniquely identify individuals,
    use ORCID ID as the value of the sameAs property of the Person type. To uniquely identify
    institutions and organizations, use ROR ID.
    
    A schema.org Person or Organization objects. To uniquely identify individuals, use ORCID
    ID as the value of the sameAs property of the Person type. To uniquely identify
    institutions and organizations, use ROR ID.
    
    Indicates the party responsible for generating and publishing the current structured data
    markup, typically in cases where the structured data is derived automatically from
    existing published content but published on a different site. For example, student
    projects and open data initiatives often re-publish existing content with more explicitly
    structured metadata. The sdPublisher property helps make such practices more explicit.
    
    A person (alive, dead, undead, or fictional).
    
    An organization such as a school, NGO, corporation, club, etc.
    """
    type: PersonOrganizationType
    affiliation: Union[OrganizationClass, None, str]
    name: str
    id: Optional[str]
    contact_point: Optional[ContactPoint]
    family_name: Optional[str]
    given_name: Optional[str]
    same_as: Optional[str]
    url: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'PersonOrganization':
        assert isinstance(obj, dict)
        type = PersonOrganizationType(obj.get("@type"))
        affiliation = from_union([OrganizationClass.from_dict, from_none, from_str], obj.get("affiliation"))
        name = from_str(obj.get("name"))
        id = from_union([from_none, from_str], obj.get("@id"))
        contact_point = from_union([ContactPoint.from_dict, from_none], obj.get("contactPoint"))
        family_name = from_union([from_none, from_str], obj.get("familyName"))
        given_name = from_union([from_none, from_str], obj.get("givenName"))
        same_as = from_union([from_none, from_str], obj.get("sameAs"))
        url = from_union([from_none, from_str], obj.get("url"))
        return PersonOrganization(type, affiliation, name, id, contact_point, family_name, given_name, same_as, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(PersonOrganizationType, self.type)
        result["affiliation"] = from_union([lambda x: to_class(OrganizationClass, x), from_none, from_str], self.affiliation)
        result["name"] = from_str(self.name)
        result["@id"] = from_union([from_none, from_str], self.id)
        result["contactPoint"] = from_union([lambda x: to_class(ContactPoint, x), from_none], self.contact_point)
        result["familyName"] = from_union([from_none, from_str], self.family_name)
        result["givenName"] = from_union([from_none, from_str], self.given_name)
        result["sameAs"] = from_union([from_none, from_str], self.same_as)
        result["url"] = from_union([from_none, from_str], self.url)
        return result


class DataProviderName(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    CSV = "CSV"
    ELASTICSEARCH = "Elasticsearch"
    GEO_JSON = "GeoJSON"
    MVT = "MVT"
    POSTGRE_SQL = "PostgreSQL"
    RASTERIO = "rasterio"
    SQ_LITE_GPKG = "SQLiteGPKG"
    XARRAY = "xarray"


@dataclass
class EOptions:
    """Coverage provider data specific options.
    
    Tile provider data specific options.
    """
    data_encoding: Optional[str]
    metadata_format: Optional[str]
    schemes: Optional[List[str]]
    zoom: Optional[Zoom]

    @staticmethod
    def from_dict(obj: Any) -> 'EOptions':
        assert isinstance(obj, dict)
        data_encoding = from_union([from_none, from_str], obj.get("DATA_ENCODING"))
        metadata_format = from_union([from_none, from_str], obj.get("metadata_format"))
        schemes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("schemes"))
        zoom = from_union([Zoom.from_dict, from_none], obj.get("zoom"))
        return EOptions(data_encoding, metadata_format, schemes, zoom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["DATA_ENCODING"] = from_union([from_none, from_str], self.data_encoding)
        result["metadata_format"] = from_union([from_none, from_str], self.metadata_format)
        result["schemes"] = from_union([lambda x: from_list(from_str, x), from_none], self.schemes)
        result["zoom"] = from_union([lambda x: to_class(Zoom, x), from_none], self.zoom)
        return result


class DataProviderType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    COVERAGE = "coverage"
    FEATURE = "feature"
    TILE = "tile"


@dataclass
class DataProvider:
    """An array of vizzToolsCore provider definition objects that describe the connections to
    the data of the dataset.
    
    CSV featureProvider
    
    GeoJSON FeatureProvider
    
    Elasticsearch FeatureProvider
    
    SQLiteGPKG featureProvider
    
    PostgreSQL featureProvider
    
    rasterio CoverageProvider
    
    xarray CoverageProvider
    
    A vizzToolsCore TileProvider definition object that describes the connection of the
    dataset data.
    
    MVT TileProvider
    """
    data: Union[DatabaseData, str]
    name: DataProviderName
    type: DataProviderType
    id_field: Optional[str]
    y_field: Optional[str]
    format: Optional[Format]
    table: Optional[str]
    time_field: Optional[str]
    geom_field: Optional[str]
    x_field: Optional[str]
    options: Optional[EOptions]

    @staticmethod
    def from_dict(obj: Any) -> 'DataProvider':
        assert isinstance(obj, dict)
        data = from_union([DatabaseData.from_dict, from_str], obj.get("data"))
        name = DataProviderName(obj.get("name"))
        type = DataProviderType(obj.get("type"))
        id_field = from_union([from_none, from_str], obj.get("id_field"))
        y_field = from_union([from_none, from_str], obj.get("y_field"))
        format = from_union([Format.from_dict, from_none], obj.get("format"))
        table = from_union([from_none, from_str], obj.get("table"))
        time_field = from_union([from_none, from_str], obj.get("time_field"))
        geom_field = from_union([from_none, from_str], obj.get("geom_field"))
        x_field = from_union([from_none, from_str], obj.get("x_field"))
        options = from_union([EOptions.from_dict, from_none], obj.get("options"))
        return DataProvider(data, name, type, id_field, y_field, format, table, time_field, geom_field, x_field, options)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([lambda x: to_class(DatabaseData, x), from_str], self.data)
        result["name"] = to_enum(DataProviderName, self.name)
        result["type"] = to_enum(DataProviderType, self.type)
        result["id_field"] = from_union([from_none, from_str], self.id_field)
        result["y_field"] = from_union([from_none, from_str], self.y_field)
        result["format"] = from_union([lambda x: to_class(Format, x), from_none], self.format)
        result["table"] = from_union([from_none, from_str], self.table)
        result["time_field"] = from_union([from_none, from_str], self.time_field)
        result["geom_field"] = from_union([from_none, from_str], self.geom_field)
        result["x_field"] = from_union([from_none, from_str], self.x_field)
        result["options"] = from_union([lambda x: to_class(EOptions, x), from_none], self.options)
        return result


class DistributionType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    DATA_DOWNLOAD = "DataDownload"


@dataclass
class DataDownload:
    """An array of schema.org DataDownload objects that describe URIs to access to the entity.
    
    A schema.org DataDownload object representing the location and file format for
    downloadable data of any type. It is best practice to give the entity a name and the
    encoding.
    """
    type: DistributionType
    content_url: str
    encoding_format: Optional[str]
    name: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'DataDownload':
        assert isinstance(obj, dict)
        type = DistributionType(obj.get("@type"))
        content_url = from_str(obj.get("contentUrl"))
        encoding_format = from_union([from_none, from_str], obj.get("encodingFormat"))
        name = from_union([from_none, from_str], obj.get("name"))
        return DataDownload(type, content_url, encoding_format, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(DistributionType, self.type)
        result["contentUrl"] = from_str(self.content_url)
        result["encodingFormat"] = from_union([from_none, from_str], self.encoding_format)
        result["name"] = from_union([from_none, from_str], self.name)
        return result


class InLanguage(Enum):
    """The language of the content or performance or used in an action. Please use one of the
    language codes from the IETF BCP 47 standard.
    
    2-digit ISO 639-1 language codes
    """
    AA = "aa"
    AB = "ab"
    AE = "ae"
    AF = "af"
    AK = "ak"
    AM = "am"
    AN = "an"
    AR = "ar"
    AS = "as"
    AV = "av"
    AY = "ay"
    AZ = "az"
    BA = "ba"
    BE = "be"
    BG = "bg"
    BH = "bh"
    BI = "bi"
    BM = "bm"
    BN = "bn"
    BO = "bo"
    BR = "br"
    BS = "bs"
    CA = "ca"
    CE = "ce"
    CH = "ch"
    CO = "co"
    CR = "cr"
    CS = "cs"
    CU = "cu"
    CV = "cv"
    CY = "cy"
    DA = "da"
    DE = "de"
    DV = "dv"
    DZ = "dz"
    EE = "ee"
    EN = "en"
    ES = "es"
    ET = "et"
    EU = "eu"
    FA = "fa"
    FF = "ff"
    FI = "fi"
    FJ = "fj"
    FO = "fo"
    FR = "fr"
    FY = "fy"
    GA = "ga"
    GD = "gd"
    GL = "gl"
    GN = "gn"
    GU = "gu"
    GV = "gv"
    HA = "ha"
    HE = "he"
    HI = "hi"
    HO = "ho"
    HR = "hr"
    HT = "ht"
    HU = "hu"
    HY = "hy"
    HZ = "hz"
    IA = "ia"
    ID = "id"
    IE = "ie"
    IG = "ig"
    II = "ii"
    IK = "ik"
    IO = "io"
    IS = "is"
    IT = "it"
    IU = "iu"
    JA = "ja"
    JV = "jv"
    KA = "ka"
    KG = "kg"
    KI = "ki"
    KJ = "kj"
    KK = "kk"
    KL = "kl"
    KM = "km"
    KN = "kn"
    KO = "ko"
    KR = "kr"
    KS = "ks"
    KU = "ku"
    KV = "kv"
    KW = "kw"
    KY = "ky"
    LA = "la"
    LB = "lb"
    LG = "lg"
    LI = "li"
    LN = "ln"
    LO = "lo"
    LT = "lt"
    LU = "lu"
    LV = "lv"
    MG = "mg"
    MH = "mh"
    MI = "mi"
    MK = "mk"
    ML = "ml"
    MN = "mn"
    MR = "mr"
    MS = "ms"
    MT = "mt"
    MY = "my"
    NA = "na"
    NB = "nb"
    ND = "nd"
    NE = "ne"
    NG = "ng"
    NL = "nl"
    NN = "nn"
    NO = "no"
    NR = "nr"
    NV = "nv"
    NY = "ny"
    OC = "oc"
    OJ = "oj"
    OM = "om"
    OR = "or"
    OS = "os"
    PA = "pa"
    PI = "pi"
    PL = "pl"
    PS = "ps"
    PT = "pt"
    QU = "qu"
    RM = "rm"
    RN = "rn"
    RO = "ro"
    RU = "ru"
    RW = "rw"
    SA = "sa"
    SC = "sc"
    SD = "sd"
    SE = "se"
    SG = "sg"
    SI = "si"
    SK = "sk"
    SL = "sl"
    SM = "sm"
    SN = "sn"
    SO = "so"
    SQ = "sq"
    SR = "sr"
    SS = "ss"
    ST = "st"
    SU = "su"
    SV = "sv"
    SW = "sw"
    TA = "ta"
    TE = "te"
    TG = "tg"
    TH = "th"
    TI = "ti"
    TK = "tk"
    TL = "tl"
    TN = "tn"
    TO = "to"
    TR = "tr"
    TS = "ts"
    TT = "tt"
    TW = "tw"
    TY = "ty"
    UG = "ug"
    UK = "uk"
    UR = "ur"
    UZ = "uz"
    VE = "ve"
    VI = "vi"
    VO = "vo"
    WA = "wa"
    WO = "wo"
    XH = "xh"
    YI = "yi"
    YO = "yo"
    ZA = "za"
    ZH = "zh"
    ZU = "zu"


class GeoType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    GEO_COORDINATES = "GeoCoordinates"
    GEO_SHAPE = "GeoShape"


@dataclass
class Geo:
    """The geo coordinates of the place.
    
    The geographic coordinates of an entity.
    
    The geographic shape of a place. A GeoShape can be described using several properties
    whose values are based on latitude/longitude pairs. Either whitespace or commas can be
    used to separate latitude and longitude; whitespace should be used when writing a list of
    several such points.
    """
    type: GeoType
    """A box is the area enclosed by the rectangle formed by two points. The first point is the
    lower corner, the second point is the upper corner. A box is expressed as two points
    separated by a space character.
    """
    box: Optional[str]
    """The latitude of a location. For example 37.42242 (WGS 84)."""
    latitude: Optional[float]
    """The longitude of a location. For example -122.08585 (WGS 84)."""
    longitude: Optional[float]

    @staticmethod
    def from_dict(obj: Any) -> 'Geo':
        assert isinstance(obj, dict)
        type = GeoType(obj.get("@type"))
        box = from_union([from_none, from_str], obj.get("box"))
        latitude = from_union([from_float, from_none], obj.get("latitude"))
        longitude = from_union([from_float, from_none], obj.get("longitude"))
        return Geo(type, box, latitude, longitude)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(GeoType, self.type)
        result["box"] = from_union([from_none, from_str], self.box)
        result["latitude"] = from_union([to_float, from_none], self.latitude)
        result["longitude"] = from_union([to_float, from_none], self.longitude)
        return result


class PlaceType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    PLACE = "Place"


@dataclass
class Place:
    """Entities that have a somewhat fixed, physical extension."""
    type: PlaceType
    name: str
    geo: Optional[Geo]
    global_location_number: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Place':
        assert isinstance(obj, dict)
        type = PlaceType(obj.get("@type"))
        name = from_str(obj.get("name"))
        geo = from_union([Geo.from_dict, from_none], obj.get("geo"))
        global_location_number = from_union([from_none, from_str], obj.get("globalLocationNumber"))
        return Place(type, name, geo, global_location_number)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(PlaceType, self.type)
        result["name"] = from_str(self.name)
        result["geo"] = from_union([lambda x: to_class(Geo, x), from_none], self.geo)
        result["globalLocationNumber"] = from_union([from_none, from_str], self.global_location_number)
        return result


class DatasetType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    DATASET = "Dataset"


class PropertyValueType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    PROPERTY_VALUE = "PropertyValue"


@dataclass
class PropertyValue:
    """Adaptation of schema.org PropertyValue for the description of the physical quantities of
    data variables (fields or parameters). Note this is non standard and includes extra
    properties from the CF standard name definition
    (http://cfconventions.org/cf-conventions/cf-conventions.html#standard-name).
    """
    type: PropertyValueType
    """Name of the property as used in the dataset."""
    name: str
    """Value of the property."""
    value: Union[List[Any], bool, float, int, Dict[str, Any], None, str]
    """Representative units of the physical quantity. Unless it is dimensionless, a variable
    with a standard_name attribute must have units which are physically equivalent (not
    necessarily identical) to the canonical units and are usually the SI units for the
    quantity. see http://cfconventions.org/cf-conventions/cf-conventions.html#standard-name
    """
    canonical_units: Optional[str]
    """The description is meant to clarify the qualifiers of the fundamental quantities such as
    which surface a quantity is defined on or what the flux sign conventions are. We don’t
    attempt to provide precise definitions of fundamental physical quantities (e.g.,
    temperature) which may be found in the literature. The description may define rules on
    the variable type, attributes and coordinates which must be complied with by any variable
    carrying that standard name.
    """
    description: Optional[str]
    """The long name of the property. Use this to provide a human readable name fro the property."""
    long_name: Optional[str]
    """Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    """
    same_as: Optional[str]
    """The name used to identify the physical quantity. A standard name contains no whitespace
    and is case sensitive. see
    http://cfconventions.org/cf-conventions/cf-conventions.html#standard-name .
    """
    standard_name: Optional[str]
    unit_text: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'PropertyValue':
        assert isinstance(obj, dict)
        type = PropertyValueType(obj.get("@type"))
        name = from_str(obj.get("name"))
        value = from_union([lambda x: from_list(lambda x: x, x), from_bool, from_float, from_int, lambda x: from_dict(lambda x: x, x), from_none, from_str], obj.get("value"))
        canonical_units = from_union([from_none, from_str], obj.get("canonical_units"))
        description = from_union([from_none, from_str], obj.get("description"))
        long_name = from_union([from_none, from_str], obj.get("long_name"))
        same_as = from_union([from_none, from_str], obj.get("sameAs"))
        standard_name = from_union([from_none, from_str], obj.get("standard_name"))
        unit_text = from_union([from_none, from_str], obj.get("unitText"))
        return PropertyValue(type, name, value, canonical_units, description, long_name, same_as, standard_name, unit_text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(PropertyValueType, self.type)
        result["name"] = from_str(self.name)
        result["value"] = from_union([lambda x: from_list(lambda x: x, x), from_bool, to_float, from_int, lambda x: from_dict(lambda x: x, x), from_none, from_str], self.value)
        result["canonical_units"] = from_union([from_none, from_str], self.canonical_units)
        result["description"] = from_union([from_none, from_str], self.description)
        result["long_name"] = from_union([from_none, from_str], self.long_name)
        result["sameAs"] = from_union([from_none, from_str], self.same_as)
        result["standard_name"] = from_union([from_none, from_str], self.standard_name)
        result["unitText"] = from_union([from_none, from_str], self.unit_text)
        return result


@dataclass
class Dataset:
    """A vizzToolsCore Dataset metadata/configuration object. This is an extended version of
    schema.org [Dataset](https://schema.org/Dataset) following the [Google structured data
    Dataset guidelines](https://developers.google.com/search/docs/data-types/dataset). Non
    schema.org extensions to this include the properties; [dataProviders](dataProviders).
    """
    identifier: Union[List[str], None, str]
    version: Union[int, None, str]
    id: str
    variable_measured: Union[PropertyValue, None, str]
    alternate_name: Union[List[str], None, str]
    citation: Union[List[str], None, str]
    spatial_coverage: Union[Place, None, str]
    license: Optional[str]
    data_providers: Optional[List[DataProvider]]
    date_modified: Optional[datetime]
    date_published: Optional[datetime]
    description: Optional[str]
    distribution: Optional[List[DataDownload]]
    funder: Optional[List[PersonOrganization]]
    has_part: Optional[List[Union[Dict[str, Any], str]]]
    context: Optional[str]
    in_language: Optional[InLanguage]
    is_based_on: Optional[str]
    is_part_of: Optional[List[Union[Dict[str, Any], str]]]
    date_created: Optional[datetime]
    measurement_technique: Optional[str]
    name: Optional[str]
    provider: Optional[List[PersonOrganization]]
    same_as: Optional[str]
    sd_publisher: Optional[List[PersonOrganization]]
    creator: Optional[List[PersonOrganization]]
    temporal_coverage: Optional[str]
    thumbnail_url: Optional[str]
    url: Optional[str]
    type: Optional[DatasetType]
    schema: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Dataset':
        assert isinstance(obj, dict)
        identifier = from_union([lambda x: from_list(from_str, x), from_none, from_str], obj.get("identifier"))
        version = from_union([from_int, from_none, from_str], obj.get("version"))
        id = from_str(obj.get("@id"))
        variable_measured = from_union([PropertyValue.from_dict, from_none, from_str], obj.get("variableMeasured"))
        alternate_name = from_union([lambda x: from_list(from_str, x), from_none, from_str], obj.get("alternateName"))
        citation = from_union([lambda x: from_list(from_str, x), from_none, from_str], obj.get("citation"))
        spatial_coverage = from_union([Place.from_dict, from_none, from_str], obj.get("spatialCoverage"))
        license = from_union([from_none, from_str], obj.get("license"))
        data_providers = from_union([lambda x: from_list(DataProvider.from_dict, x), from_none], obj.get("dataProviders"))
        date_modified = from_union([from_datetime, from_none], obj.get("dateModified"))
        date_published = from_union([from_datetime, from_none], obj.get("datePublished"))
        description = from_union([from_none, from_str], obj.get("description"))
        distribution = from_union([lambda x: from_list(DataDownload.from_dict, x), from_none], obj.get("distribution"))
        funder = from_union([lambda x: from_list(PersonOrganization.from_dict, x), from_none], obj.get("funder"))
        has_part = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], obj.get("hasPart"))
        context = from_union([from_none, from_str], obj.get("@context"))
        in_language = from_union([InLanguage, from_none], obj.get("inLanguage"))
        is_based_on = from_union([from_none, from_str], obj.get("isBasedOn"))
        is_part_of = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], obj.get("isPartOf"))
        date_created = from_union([from_datetime, from_none], obj.get("dateCreated"))
        measurement_technique = from_union([from_none, from_str], obj.get("measurementTechnique"))
        name = from_union([from_none, from_str], obj.get("name"))
        provider = from_union([lambda x: from_list(PersonOrganization.from_dict, x), from_none], obj.get("provider"))
        same_as = from_union([from_none, from_str], obj.get("sameAs"))
        sd_publisher = from_union([lambda x: from_list(PersonOrganization.from_dict, x), from_none], obj.get("sdPublisher"))
        creator = from_union([lambda x: from_list(PersonOrganization.from_dict, x), from_none], obj.get("creator"))
        temporal_coverage = from_union([from_none, from_str], obj.get("temporalCoverage"))
        thumbnail_url = from_union([from_none, from_str], obj.get("thumbnailUrl"))
        url = from_union([from_none, from_str], obj.get("url"))
        type = from_union([DatasetType, from_none], obj.get("@type"))
        schema = from_union([from_none, from_str], obj.get("$schema"))
        return Dataset(identifier, version, id, variable_measured, alternate_name, citation, spatial_coverage, license, data_providers, date_modified, date_published, description, distribution, funder, has_part, context, in_language, is_based_on, is_part_of, date_created, measurement_technique, name, provider, same_as, sd_publisher, creator, temporal_coverage, thumbnail_url, url, type, schema)

    def to_dict(self) -> dict:
        result: dict = {}
        result["identifier"] = from_union([lambda x: from_list(from_str, x), from_none, from_str], self.identifier)
        result["version"] = from_union([from_int, from_none, from_str], self.version)
        result["@id"] = from_str(self.id)
        result["variableMeasured"] = from_union([lambda x: to_class(PropertyValue, x), from_none, from_str], self.variable_measured)
        result["alternateName"] = from_union([lambda x: from_list(from_str, x), from_none, from_str], self.alternate_name)
        result["citation"] = from_union([lambda x: from_list(from_str, x), from_none, from_str], self.citation)
        result["spatialCoverage"] = from_union([lambda x: to_class(Place, x), from_none, from_str], self.spatial_coverage)
        result["license"] = from_union([from_none, from_str], self.license)
        result["dataProviders"] = from_union([lambda x: from_list(lambda x: to_class(DataProvider, x), x), from_none], self.data_providers)
        result["dateModified"] = from_union([lambda x: x.isoformat(), from_none], self.date_modified)
        result["datePublished"] = from_union([lambda x: x.isoformat(), from_none], self.date_published)
        result["description"] = from_union([from_none, from_str], self.description)
        result["distribution"] = from_union([lambda x: from_list(lambda x: to_class(DataDownload, x), x), from_none], self.distribution)
        result["funder"] = from_union([lambda x: from_list(lambda x: to_class(PersonOrganization, x), x), from_none], self.funder)
        result["hasPart"] = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], self.has_part)
        result["@context"] = from_union([from_none, from_str], self.context)
        result["inLanguage"] = from_union([lambda x: to_enum(InLanguage, x), from_none], self.in_language)
        result["isBasedOn"] = from_union([from_none, from_str], self.is_based_on)
        result["isPartOf"] = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], self.is_part_of)
        result["dateCreated"] = from_union([lambda x: x.isoformat(), from_none], self.date_created)
        result["measurementTechnique"] = from_union([from_none, from_str], self.measurement_technique)
        result["name"] = from_union([from_none, from_str], self.name)
        result["provider"] = from_union([lambda x: from_list(lambda x: to_class(PersonOrganization, x), x), from_none], self.provider)
        result["sameAs"] = from_union([from_none, from_str], self.same_as)
        result["sdPublisher"] = from_union([lambda x: from_list(lambda x: to_class(PersonOrganization, x), x), from_none], self.sd_publisher)
        result["creator"] = from_union([lambda x: from_list(lambda x: to_class(PersonOrganization, x), x), from_none], self.creator)
        result["temporalCoverage"] = from_union([from_none, from_str], self.temporal_coverage)
        result["thumbnailUrl"] = from_union([from_none, from_str], self.thumbnail_url)
        result["url"] = from_union([from_none, from_str], self.url)
        result["@type"] = from_union([lambda x: to_enum(DatasetType, x), from_none], self.type)
        result["$schema"] = from_union([from_none, from_str], self.schema)
        return result


@dataclass
class Organization:
    """An organization such as a school, NGO, corporation, club, etc."""
    type: OrganizationType
    name: str
    id: Optional[str]
    contact_point: Optional[ContactPoint]
    same_as: Optional[str]
    url: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Organization':
        assert isinstance(obj, dict)
        type = OrganizationType(obj.get("@type"))
        name = from_str(obj.get("name"))
        id = from_union([from_none, from_str], obj.get("@id"))
        contact_point = from_union([ContactPoint.from_dict, from_none], obj.get("contactPoint"))
        same_as = from_union([from_none, from_str], obj.get("sameAs"))
        url = from_union([from_none, from_str], obj.get("url"))
        return Organization(type, name, id, contact_point, same_as, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(OrganizationType, self.type)
        result["name"] = from_str(self.name)
        result["@id"] = from_union([from_none, from_str], self.id)
        result["contactPoint"] = from_union([lambda x: to_class(ContactPoint, x), from_none], self.contact_point)
        result["sameAs"] = from_union([from_none, from_str], self.same_as)
        result["url"] = from_union([from_none, from_str], self.url)
        return result


class PersonType(Enum):
    """URI pointing to the data.
    
    String representing a URI.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Provider definition name.
    
    Provider definition type.
    
    Time field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Identifier field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    URI of the JSON schema of this object.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    The Global Location Number (GLN, sometimes also referred to as International Location
    Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit
    number used to identify parties and physical locations.
    
    The data in the dataset covers a specific time interval. Only include this property if
    the dataset has a temporal dimension. Schema.org uses the ISO 8601 standard to describe
    time intervals and time points. You can describe dates differently depending upon the
    dataset interval. Indicate open-ended intervals with two decimal points (..). TODO:
    adjust validation for these specific cases!
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use [SI prefix symbols](https://en.wikipedia.org/wiki/Metric_prefix).
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    PERSON = "Person"


@dataclass
class Person:
    """A person (alive, dead, undead, or fictional)."""
    type: PersonType
    affiliation: Union[OrganizationClass, None, str]
    name: str
    id: Optional[str]
    family_name: Optional[str]
    given_name: Optional[str]
    same_as: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Person':
        assert isinstance(obj, dict)
        type = PersonType(obj.get("@type"))
        affiliation = from_union([OrganizationClass.from_dict, from_none, from_str], obj.get("affiliation"))
        name = from_str(obj.get("name"))
        id = from_union([from_none, from_str], obj.get("@id"))
        family_name = from_union([from_none, from_str], obj.get("familyName"))
        given_name = from_union([from_none, from_str], obj.get("givenName"))
        same_as = from_union([from_none, from_str], obj.get("sameAs"))
        return Person(type, affiliation, name, id, family_name, given_name, same_as)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(PersonType, self.type)
        result["affiliation"] = from_union([lambda x: to_class(OrganizationClass, x), from_none, from_str], self.affiliation)
        result["name"] = from_str(self.name)
        result["@id"] = from_union([from_none, from_str], self.id)
        result["familyName"] = from_union([from_none, from_str], self.family_name)
        result["givenName"] = from_union([from_none, from_str], self.given_name)
        result["sameAs"] = from_union([from_none, from_str], self.same_as)
        return result


def coverage_provider_from_dict(s: Any) -> CoverageProvider:
    return CoverageProvider.from_dict(s)


def coverage_provider_to_dict(x: CoverageProvider) -> Any:
    return to_class(CoverageProvider, x)


def feature_provider_from_dict(s: Any) -> FeatureProvider:
    return FeatureProvider.from_dict(s)


def feature_provider_to_dict(x: FeatureProvider) -> Any:
    return to_class(FeatureProvider, x)


def tile_provider_from_dict(s: Any) -> TileProvider:
    return TileProvider.from_dict(s)


def tile_provider_to_dict(x: TileProvider) -> Any:
    return to_class(TileProvider, x)


def dataset_from_dict(s: Any) -> Dataset:
    return Dataset.from_dict(s)


def dataset_to_dict(x: Dataset) -> Any:
    return to_class(Dataset, x)


def organization_from_dict(s: Any) -> Organization:
    return Organization.from_dict(s)


def organization_to_dict(x: Organization) -> Any:
    return to_class(Organization, x)


def person_from_dict(s: Any) -> Person:
    return Person.from_dict(s)


def person_to_dict(x: Person) -> Any:
    return to_class(Person, x)
