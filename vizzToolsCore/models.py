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
#     result = vtc_dataset_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, List, Any, Union, Dict, TypeVar, Callable, Type, cast
from enum import Enum
from datetime import datetime
import dateutil.parser


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
class DatabaseData:
    """Object defining database connection."""
    dbname: Optional[str] = None
    host: Optional[str] = None
    password: Optional[str] = None
    search_path: Optional[List[str]] = None
    user: Optional[str] = None

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


@dataclass
class Format:
    """Provider data format."""
    mimetype: Optional[str] = None
    name: Optional[str] = None

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


@dataclass
class Zoom:
    """Minimum and maximum zoom levels."""
    max: Optional[int] = None
    min: Optional[int] = None

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
class EOptions:
    """Coverage provider data specific options.
    
    Tile provider data specific options.
    """
    data_encoding: Optional[str] = None
    metadata_format: Optional[str] = None
    schemes: Optional[List[str]] = None
    zoom: Optional[Zoom] = None

    @staticmethod
    def from_dict(obj: Any) -> 'EOptions':
        assert isinstance(obj, dict)
        data_encoding = from_union([from_str, from_none], obj.get("DATA_ENCODING"))
        metadata_format = from_union([from_str, from_none], obj.get("metadata_format"))
        schemes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("schemes"))
        zoom = from_union([Zoom.from_dict, from_none], obj.get("zoom"))
        return EOptions(data_encoding, metadata_format, schemes, zoom)

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
    name: str
    type: TypeEnum
    id_field: Optional[str] = None
    time_field: Optional[str] = None
    table: Optional[str] = None
    geom_field: Optional[str] = None
    format: Optional[Format] = None
    options: Optional[EOptions] = None
    x_field: Optional[str] = None
    y_field: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DataProvider':
        assert isinstance(obj, dict)
        data = from_union([from_str, DatabaseData.from_dict], obj.get("data"))
        name = from_str(obj.get("name"))
        type = TypeEnum(obj.get("type"))
        id_field = from_union([from_str, from_none], obj.get("id_field"))
        time_field = from_union([from_str, from_none], obj.get("time_field"))
        table = from_union([from_str, from_none], obj.get("table"))
        geom_field = from_union([from_str, from_none], obj.get("geom_field"))
        format = from_union([Format.from_dict, from_none], obj.get("format"))
        options = from_union([EOptions.from_dict, from_none], obj.get("options"))
        x_field = from_union([from_str, from_none], obj.get("x_field"))
        y_field = from_union([from_str, from_none], obj.get("y_field"))
        return DataProvider(data, name, type, id_field, time_field, table, geom_field, format, options, x_field, y_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([from_str, lambda x: to_class(DatabaseData, x)], self.data)
        result["name"] = from_str(self.name)
        result["type"] = to_enum(TypeEnum, self.type)
        result["id_field"] = from_union([from_str, from_none], self.id_field)
        result["time_field"] = from_union([from_str, from_none], self.time_field)
        result["table"] = from_union([from_str, from_none], self.table)
        result["geom_field"] = from_union([from_str, from_none], self.geom_field)
        result["format"] = from_union([lambda x: to_class(Format, x), from_none], self.format)
        result["options"] = from_union([lambda x: to_class(EOptions, x), from_none], self.options)
        result["x_field"] = from_union([from_str, from_none], self.x_field)
        result["y_field"] = from_union([from_str, from_none], self.y_field)
        return result


@dataclass
class Link:
    """An array of schema.org DataDownload objects that describe URIs to access description,
    metadata and data of the dataset. Use `name` to indicate the information type.
    
    A schema.org DataDownload object representing the location and file format for
    downloadable data.
    
    An array of schema.org DataDownload objects that describe URIs to access to the entity.
    """
    type: Any
    content_url: Any
    name: Any

    @staticmethod
    def from_dict(obj: Any) -> 'Link':
        assert isinstance(obj, dict)
        type = obj.get("@type")
        content_url = obj.get("contentUrl")
        name = obj.get("name")
        return Link(type, content_url, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = self.type
        result["contentUrl"] = self.content_url
        result["name"] = self.name
        return result


class ContactPointType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    URI pointing to the data.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases
    when the dataset or description is a simple republication of materials published
    elsewhere. The value of sameAs needs to unambiguously indicate the datasets identity - in
    other words two different datasets should not use the same URL as sameAs value.
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Type of this object.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    CONTACT_POINT = "contactPoint"


@dataclass
class ContactPoint:
    type: ContactPointType
    email: str
    contact_type: Optional[str] = None
    telephone: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ContactPoint':
        assert isinstance(obj, dict)
        type = ContactPointType(obj.get("@type"))
        email = from_str(obj.get("email"))
        contact_type = from_union([from_str, from_none], obj.get("contactType"))
        telephone = from_union([from_str, from_none], obj.get("telephone"))
        return ContactPoint(type, email, contact_type, telephone)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(ContactPointType, self.type)
        result["email"] = from_str(self.email)
        result["contactType"] = from_union([from_str, from_none], self.contact_type)
        result["telephone"] = from_union([from_str, from_none], self.telephone)
        return result


class SDPublisherType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    URI pointing to the data.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases
    when the dataset or description is a simple republication of materials published
    elsewhere. The value of sameAs needs to unambiguously indicate the datasets identity - in
    other words two different datasets should not use the same URL as sameAs value.
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Type of this object.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    ORGANIZATION = "Organization"
    PERSON = "Person"


@dataclass
class SDPublisher:
    """An array of schema.org Person or Organization objects. To uniquely identify individuals,
    use ORCID ID as the value of the sameAs property of the Person type. To uniquely identify
    institutions and organizations, use ROR ID.
    
    Indicates the party responsible for generating and publishing the current structured data
    markup, typically in cases where the structured data is derived automatically from
    existing published content but published on a different site. For example, student
    projects and open data initiatives often re-publish existing content with more explicitly
    structured metadata. The sdPublisher property helps make such practices more explicit.
    
    A person (alive, dead, undead, or fictional).
    
    An organization such as a school, NGO, corporation, club, etc.
    """
    id: Any
    type: SDPublisherType
    affiliation: Any
    name: str
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    same_as: Optional[str] = None
    contact_point: Optional[ContactPoint] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SDPublisher':
        assert isinstance(obj, dict)
        id = obj.get("@id")
        type = SDPublisherType(obj.get("@type"))
        affiliation = obj.get("affiliation")
        name = from_str(obj.get("name"))
        family_name = from_union([from_str, from_none], obj.get("familyName"))
        given_name = from_union([from_str, from_none], obj.get("givenName"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        contact_point = from_union([ContactPoint.from_dict, from_none], obj.get("contactPoint"))
        url = from_union([from_str, from_none], obj.get("url"))
        return SDPublisher(id, type, affiliation, name, family_name, given_name, same_as, contact_point, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@id"] = self.id
        result["@type"] = to_enum(SDPublisherType, self.type)
        result["affiliation"] = self.affiliation
        result["name"] = from_str(self.name)
        result["familyName"] = from_union([from_str, from_none], self.family_name)
        result["givenName"] = from_union([from_str, from_none], self.given_name)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["contactPoint"] = from_union([lambda x: to_class(ContactPoint, x), from_none], self.contact_point)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class DataDownload:
    """An array of schema.org DataDownload objects that describe URIs to access description,
    metadata and data of the dataset. Use `name` to indicate the information type.
    
    A schema.org DataDownload object representing the location and file format for
    downloadable data.
    
    An array of schema.org DataDownload objects that describe URIs to access to the entity.
    """
    type: Any
    content_url: Any

    @staticmethod
    def from_dict(obj: Any) -> 'DataDownload':
        assert isinstance(obj, dict)
        type = obj.get("@type")
        content_url = obj.get("contentUrl")
        return DataDownload(type, content_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = self.type
        result["contentUrl"] = self.content_url
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
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    URI pointing to the data.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases
    when the dataset or description is a simple republication of materials published
    elsewhere. The value of sameAs needs to unambiguously indicate the datasets identity - in
    other words two different datasets should not use the same URL as sameAs value.
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Type of this object.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
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
    """The latitude of a location. For example 37.42242 (WGS 84)."""
    latitude: Optional[float] = None
    """The longitude of a location. For example -122.08585 (WGS 84)."""
    longitude: Optional[float] = None
    """A box is the area enclosed by the rectangle formed by two points. The first point is the
    lower corner, the second point is the upper corner. A box is expressed as two points
    separated by a space character.
    """
    box: Optional[str] = None

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
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    URI pointing to the data.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases
    when the dataset or description is a simple republication of materials published
    elsewhere. The value of sameAs needs to unambiguously indicate the datasets identity - in
    other words two different datasets should not use the same URL as sameAs value.
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Type of this object.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
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
    geo: Geo

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


class MetadatumType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    URI pointing to the data.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases
    when the dataset or description is a simple republication of materials published
    elsewhere. The value of sameAs needs to unambiguously indicate the datasets identity - in
    other words two different datasets should not use the same URL as sameAs value.
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Type of this object.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    DATASET = "Dataset"


class PropertyValueType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    URI pointing to the data.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases
    when the dataset or description is a simple republication of materials published
    elsewhere. The value of sameAs needs to unambiguously indicate the datasets identity - in
    other words two different datasets should not use the same URL as sameAs value.
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Type of this object.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
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
    canonical_units: Optional[str] = None
    """The description is meant to clarify the qualifiers of the fundamental quantities such as
    which surface a quantity is defined on or what the flux sign conventions are. We don’t
    attempt to provide precise definitions of fundamental physical quantities (e.g.,
    temperature) which may be found in the literature. The description may define rules on
    the variable type, attributes and coordinates which must be complied with by any variable
    carrying that standard name.
    """
    description: Optional[str] = None
    """The long name of the property. Use this to provide a human readable name fro the property."""
    long_name: Optional[str] = None
    """Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    """
    same_as: Optional[str] = None
    """The name used to identify the physical quantity. A standard name contains no whitespace
    and is case sensitive. see
    http://cfconventions.org/cf-conventions/cf-conventions.html#standard-name .
    """
    standard_name: Optional[str] = None
    unit_text: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PropertyValue':
        assert isinstance(obj, dict)
        type = PropertyValueType(obj.get("@type"))
        name = from_str(obj.get("name"))
        value = from_union([from_float, from_int, from_bool, lambda x: from_dict(lambda x: x, x), lambda x: from_list(lambda x: x, x), from_str, from_none], obj.get("value"))
        canonical_units = from_union([from_str, from_none], obj.get("canonical_units"))
        description = from_union([from_str, from_none], obj.get("description"))
        long_name = from_union([from_str, from_none], obj.get("long_name"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        standard_name = from_union([from_str, from_none], obj.get("standard_name"))
        unit_text = from_union([from_str, from_none], obj.get("unitText"))
        return PropertyValue(type, name, value, canonical_units, description, long_name, same_as, standard_name, unit_text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(PropertyValueType, self.type)
        result["name"] = from_str(self.name)
        result["value"] = from_union([to_float, from_int, from_bool, lambda x: from_dict(lambda x: x, x), lambda x: from_list(lambda x: x, x), from_str, from_none], self.value)
        result["canonical_units"] = from_union([from_str, from_none], self.canonical_units)
        result["description"] = from_union([from_str, from_none], self.description)
        result["long_name"] = from_union([from_str, from_none], self.long_name)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["standard_name"] = from_union([from_str, from_none], self.standard_name)
        result["unitText"] = from_union([from_str, from_none], self.unit_text)
        return result


@dataclass
class Dataset:
    """An array of schema.org Dataset objects that describe the dataset
    
    A schema.org Dataset metadata object that describes the dataset.
    """
    schema: str
    context: str
    id: Any
    type: MetadatumType
    alternate_name: Union[List[str], None, str]
    citation: Union[List[str], None, str]
    description: str
    identifier: Union[List[str], None, str]
    name: str
    spatial_coverage: Union[Place, None, str]
    variable_measured: Union[PropertyValue, None, str]
    version: Union[int, None, str]
    creator: Optional[List[SDPublisher]] = None
    date_published: Optional[datetime] = None
    distribution: Optional[List[DataDownload]] = None
    funder: Optional[List[SDPublisher]] = None
    has_part: Optional[List[Union[Dict[str, Any], str]]] = None
    in_language: Optional[InLanguage] = None
    is_based_on: Optional[str] = None
    is_part_of: Optional[List[Union[Dict[str, Any], str]]] = None
    license: Optional[str] = None
    measurement_technique: Optional[str] = None
    provider: Optional[List[SDPublisher]] = None
    """Use the sameAs property to indicate the most canonical URLs for the original in cases
    when the dataset or description is a simple republication of materials published
    elsewhere. The value of sameAs needs to unambiguously indicate the datasets identity - in
    other words two different datasets should not use the same URL as sameAs value.
    """
    same_as: Optional[str] = None
    temporal_coverage: Optional[datetime] = None
    thumbnail_url: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Dataset':
        assert isinstance(obj, dict)
        schema = from_str(obj.get("$schema"))
        context = from_str(obj.get("@context"))
        id = obj.get("@id")
        type = MetadatumType(obj.get("@type"))
        alternate_name = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("alternateName"))
        citation = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("citation"))
        description = from_str(obj.get("description"))
        identifier = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("identifier"))
        name = from_str(obj.get("name"))
        spatial_coverage = from_union([Place.from_dict, from_str, from_none], obj.get("spatialCoverage"))
        variable_measured = from_union([PropertyValue.from_dict, from_str, from_none], obj.get("variableMeasured"))
        version = from_union([from_int, from_str, from_none], obj.get("version"))
        creator = from_union([lambda x: from_list(SDPublisher.from_dict, x), from_none], obj.get("creator"))
        date_published = from_union([from_datetime, from_none], obj.get("datePublished"))
        distribution = from_union([lambda x: from_list(DataDownload.from_dict, x), from_none], obj.get("distribution"))
        funder = from_union([lambda x: from_list(SDPublisher.from_dict, x), from_none], obj.get("funder"))
        has_part = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], obj.get("hasPart"))
        in_language = from_union([InLanguage, from_none], obj.get("inLanguage"))
        is_based_on = from_union([from_str, from_none], obj.get("isBasedOn"))
        is_part_of = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], obj.get("isPartOf"))
        license = from_union([from_str, from_none], obj.get("license"))
        measurement_technique = from_union([from_str, from_none], obj.get("measurementTechnique"))
        provider = from_union([lambda x: from_list(SDPublisher.from_dict, x), from_none], obj.get("provider"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        temporal_coverage = from_union([from_datetime, from_none], obj.get("temporalCoverage"))
        thumbnail_url = from_union([from_str, from_none], obj.get("thumbnailUrl"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Dataset(schema, context, id, type, alternate_name, citation, description, identifier, name, spatial_coverage, variable_measured, version, creator, date_published, distribution, funder, has_part, in_language, is_based_on, is_part_of, license, measurement_technique, provider, same_as, temporal_coverage, thumbnail_url, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["$schema"] = from_str(self.schema)
        result["@context"] = from_str(self.context)
        result["@id"] = self.id
        result["@type"] = to_enum(MetadatumType, self.type)
        result["alternateName"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.alternate_name)
        result["citation"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.citation)
        result["description"] = from_str(self.description)
        result["identifier"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.identifier)
        result["name"] = from_str(self.name)
        result["spatialCoverage"] = from_union([lambda x: to_class(Place, x), from_str, from_none], self.spatial_coverage)
        result["variableMeasured"] = from_union([lambda x: to_class(PropertyValue, x), from_str, from_none], self.variable_measured)
        result["version"] = from_union([from_int, from_str, from_none], self.version)
        result["creator"] = from_union([lambda x: from_list(lambda x: to_class(SDPublisher, x), x), from_none], self.creator)
        result["datePublished"] = from_union([lambda x: x.isoformat(), from_none], self.date_published)
        result["distribution"] = from_union([lambda x: from_list(lambda x: to_class(DataDownload, x), x), from_none], self.distribution)
        result["funder"] = from_union([lambda x: from_list(lambda x: to_class(SDPublisher, x), x), from_none], self.funder)
        result["hasPart"] = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], self.has_part)
        result["inLanguage"] = from_union([lambda x: to_enum(InLanguage, x), from_none], self.in_language)
        result["isBasedOn"] = from_union([from_str, from_none], self.is_based_on)
        result["isPartOf"] = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], self.is_part_of)
        result["license"] = from_union([from_str, from_none], self.license)
        result["measurementTechnique"] = from_union([from_str, from_none], self.measurement_technique)
        result["provider"] = from_union([lambda x: from_list(lambda x: to_class(SDPublisher, x), x), from_none], self.provider)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["temporalCoverage"] = from_union([lambda x: x.isoformat(), from_none], self.temporal_coverage)
        result["thumbnailUrl"] = from_union([from_str, from_none], self.thumbnail_url)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class VtcDatasetType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    URI pointing to the data.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases
    when the dataset or description is a simple republication of materials published
    elsewhere. The value of sameAs needs to unambiguously indicate the datasets identity - in
    other words two different datasets should not use the same URL as sameAs value.
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Type of this object.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    VCS_DATASET = "VcsDataset"


@dataclass
class VtcDataset:
    """A vizzToolsCore Dataset configuration object."""
    schema: str
    context: str
    id: Any
    type: VtcDatasetType
    data_providers: Optional[List[DataProvider]] = None
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    links: Optional[List[Link]] = None
    metadata: Optional[List[Dataset]] = None
    sd_publisher: Optional[SDPublisher] = None

    @staticmethod
    def from_dict(obj: Any) -> 'VtcDataset':
        assert isinstance(obj, dict)
        schema = from_str(obj.get("$schema"))
        context = from_str(obj.get("@context"))
        id = obj.get("@id")
        type = VtcDatasetType(obj.get("@type"))
        data_providers = from_union([lambda x: from_list(DataProvider.from_dict, x), from_none], obj.get("dataProviders"))
        date_created = from_union([from_datetime, from_none], obj.get("dateCreated"))
        date_modified = from_union([from_datetime, from_none], obj.get("dateModified"))
        links = from_union([lambda x: from_list(Link.from_dict, x), from_none], obj.get("links"))
        metadata = from_union([lambda x: from_list(Dataset.from_dict, x), from_none], obj.get("metadata"))
        sd_publisher = from_union([SDPublisher.from_dict, from_none], obj.get("sdPublisher"))
        return VtcDataset(schema, context, id, type, data_providers, date_created, date_modified, links, metadata, sd_publisher)

    def to_dict(self) -> dict:
        result: dict = {}
        result["$schema"] = from_str(self.schema)
        result["@context"] = from_str(self.context)
        result["@id"] = self.id
        result["@type"] = to_enum(VtcDatasetType, self.type)
        result["dataProviders"] = from_union([lambda x: from_list(lambda x: to_class(DataProvider, x), x), from_none], self.data_providers)
        result["dateCreated"] = from_union([lambda x: x.isoformat(), from_none], self.date_created)
        result["dateModified"] = from_union([lambda x: x.isoformat(), from_none], self.date_modified)
        result["links"] = from_union([lambda x: from_list(lambda x: to_class(Link, x), x), from_none], self.links)
        result["metadata"] = from_union([lambda x: from_list(lambda x: to_class(Dataset, x), x), from_none], self.metadata)
        result["sdPublisher"] = from_union([lambda x: to_class(SDPublisher, x), from_none], self.sd_publisher)
        return result


def vtc_dataset_from_dict(s: Any) -> VtcDataset:
    return VtcDataset.from_dict(s)


def vtc_dataset_to_dict(x: VtcDataset) -> Any:
    return to_class(VtcDataset, x)
