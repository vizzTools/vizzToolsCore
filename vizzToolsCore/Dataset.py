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
#     result = dataset_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, Any, Union, List, Dict, TypeVar, Type, cast, Callable
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


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


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


class ContactPointType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    URI pointing to the data.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
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
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    CONTACT_POINT = "ContactPoint"


class ContactPoint:
    """A contact point—for example, a Customer Complaints department."""
    type: ContactPointType
    contact_type: Optional[str]
    email: str
    telephone: Optional[str]

    def __init__(self, type: ContactPointType, contact_type: Optional[str], email: str, telephone: Optional[str]) -> None:
        self.type = type
        self.contact_type = contact_type
        self.email = email
        self.telephone = telephone

    @staticmethod
    def from_dict(obj: Any) -> 'ContactPoint':
        assert isinstance(obj, dict)
        type = ContactPointType(obj.get("@type"))
        contact_type = from_union([from_str, from_none], obj.get("contactType"))
        email = from_str(obj.get("email"))
        telephone = from_union([from_str, from_none], obj.get("telephone"))
        return ContactPoint(type, contact_type, email, telephone)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(ContactPointType, self.type)
        result["contactType"] = from_union([from_str, from_none], self.contact_type)
        result["email"] = from_str(self.email)
        result["telephone"] = from_union([from_str, from_none], self.telephone)
        return result


class OrganizationType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    URI pointing to the data.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
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
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    ORGANIZATION = "Organization"


class Organization:
    """An organization such as a school, NGO, corporation, club, etc."""
    id: Optional[str]
    type: OrganizationType
    contact_point: Optional[ContactPoint]
    name: str
    same_as: Optional[str]
    url: Optional[str]

    def __init__(self, id: Optional[str], type: OrganizationType, contact_point: Optional[ContactPoint], name: str, same_as: Optional[str], url: Optional[str]) -> None:
        self.id = id
        self.type = type
        self.contact_point = contact_point
        self.name = name
        self.same_as = same_as
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Organization':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("@id"))
        type = OrganizationType(obj.get("@type"))
        contact_point = from_union([ContactPoint.from_dict, from_none], obj.get("contactPoint"))
        name = from_str(obj.get("name"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Organization(id, type, contact_point, name, same_as, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@id"] = from_union([from_str, from_none], self.id)
        result["@type"] = to_enum(OrganizationType, self.type)
        result["contactPoint"] = from_union([lambda x: to_class(ContactPoint, x), from_none], self.contact_point)
        result["name"] = from_str(self.name)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class SDPublisherType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    URI pointing to the data.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
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
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    ORGANIZATION = "Organization"
    PERSON = "Person"


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
    id: Optional[str]
    type: SDPublisherType
    affiliation: Union[Organization, None, str]
    family_name: Optional[str]
    given_name: Optional[str]
    name: str
    same_as: Optional[str]
    contact_point: Optional[ContactPoint]
    url: Optional[str]

    def __init__(self, id: Optional[str], type: SDPublisherType, affiliation: Union[Organization, None, str], family_name: Optional[str], given_name: Optional[str], name: str, same_as: Optional[str], contact_point: Optional[ContactPoint], url: Optional[str]) -> None:
        self.id = id
        self.type = type
        self.affiliation = affiliation
        self.family_name = family_name
        self.given_name = given_name
        self.name = name
        self.same_as = same_as
        self.contact_point = contact_point
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'SDPublisher':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("@id"))
        type = SDPublisherType(obj.get("@type"))
        affiliation = from_union([Organization.from_dict, from_str, from_none], obj.get("affiliation"))
        family_name = from_union([from_str, from_none], obj.get("familyName"))
        given_name = from_union([from_str, from_none], obj.get("givenName"))
        name = from_str(obj.get("name"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        contact_point = from_union([ContactPoint.from_dict, from_none], obj.get("contactPoint"))
        url = from_union([from_str, from_none], obj.get("url"))
        return SDPublisher(id, type, affiliation, family_name, given_name, name, same_as, contact_point, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@id"] = from_union([from_str, from_none], self.id)
        result["@type"] = to_enum(SDPublisherType, self.type)
        result["affiliation"] = from_union([lambda x: to_class(Organization, x), from_str, from_none], self.affiliation)
        result["familyName"] = from_union([from_str, from_none], self.family_name)
        result["givenName"] = from_union([from_str, from_none], self.given_name)
        result["name"] = from_str(self.name)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["contactPoint"] = from_union([lambda x: to_class(ContactPoint, x), from_none], self.contact_point)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


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


class EOptions:
    """Coverage provider data specific options.
    
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
    id_field: Optional[str]
    name: str
    type: TypeEnum
    time_field: Optional[str]
    table: Optional[str]
    geom_field: Optional[str]
    format: Optional[Format]
    options: Optional[EOptions]
    x_field: Optional[str]
    y_field: Optional[str]

    def __init__(self, data: Union[DatabaseData, str], id_field: Optional[str], name: str, type: TypeEnum, time_field: Optional[str], table: Optional[str], geom_field: Optional[str], format: Optional[Format], options: Optional[EOptions], x_field: Optional[str], y_field: Optional[str]) -> None:
        self.data = data
        self.id_field = id_field
        self.name = name
        self.type = type
        self.time_field = time_field
        self.table = table
        self.geom_field = geom_field
        self.format = format
        self.options = options
        self.x_field = x_field
        self.y_field = y_field

    @staticmethod
    def from_dict(obj: Any) -> 'DataProvider':
        assert isinstance(obj, dict)
        data = from_union([from_str, DatabaseData.from_dict], obj.get("data"))
        id_field = from_union([from_str, from_none], obj.get("id_field"))
        name = from_str(obj.get("name"))
        type = TypeEnum(obj.get("type"))
        time_field = from_union([from_str, from_none], obj.get("time_field"))
        table = from_union([from_str, from_none], obj.get("table"))
        geom_field = from_union([from_str, from_none], obj.get("geom_field"))
        format = from_union([Format.from_dict, from_none], obj.get("format"))
        options = from_union([EOptions.from_dict, from_none], obj.get("options"))
        x_field = from_union([from_str, from_none], obj.get("x_field"))
        y_field = from_union([from_str, from_none], obj.get("y_field"))
        return DataProvider(data, id_field, name, type, time_field, table, geom_field, format, options, x_field, y_field)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_union([from_str, lambda x: to_class(DatabaseData, x)], self.data)
        result["id_field"] = from_union([from_str, from_none], self.id_field)
        result["name"] = from_str(self.name)
        result["type"] = to_enum(TypeEnum, self.type)
        result["time_field"] = from_union([from_str, from_none], self.time_field)
        result["table"] = from_union([from_str, from_none], self.table)
        result["geom_field"] = from_union([from_str, from_none], self.geom_field)
        result["format"] = from_union([lambda x: to_class(Format, x), from_none], self.format)
        result["options"] = from_union([lambda x: to_class(EOptions, x), from_none], self.options)
        result["x_field"] = from_union([from_str, from_none], self.x_field)
        result["y_field"] = from_union([from_str, from_none], self.y_field)
        return result


class DataDownload:
    """An array of schema.org DataDownload objects that describe URIs to access to the entity.
    
    A schema.org DataDownload object representing the location and file format for
    downloadable data of any type. It is best practice to give the entity a name and the
    encoding.
    """
    type: Any
    content_url: Any

    def __init__(self, type: Any, content_url: Any) -> None:
        self.type = type
        self.content_url = content_url

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
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    URI pointing to the data.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
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
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
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
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    URI pointing to the data.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
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
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    PLACE = "Place"


class Place:
    """Entities that have a somewhat fixed, physical extension."""
    type: PlaceType
    geo: Geo
    global_location_number: Optional[str]
    name: Optional[str]

    def __init__(self, type: PlaceType, geo: Geo, global_location_number: Optional[str], name: Optional[str]) -> None:
        self.type = type
        self.geo = geo
        self.global_location_number = global_location_number
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Place':
        assert isinstance(obj, dict)
        type = PlaceType(obj.get("@type"))
        geo = Geo.from_dict(obj.get("geo"))
        global_location_number = from_union([from_str, from_none], obj.get("globalLocationNumber"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Place(type, geo, global_location_number, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(PlaceType, self.type)
        result["geo"] = to_class(Geo, self.geo)
        result["globalLocationNumber"] = from_union([from_str, from_none], self.global_location_number)
        result["name"] = from_union([from_str, from_none], self.name)
        return result


class DatasetType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    URI pointing to the data.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
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
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
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
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    URI pointing to the data.
    
    Use the isBasedOn property in cases where the republished dataset (including its
    metadata) has been changed significantly. When a dataset derives from or aggregates
    several originals, use the isBasedOn property. TODO: Align with Google Dataset
    guidelines
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive (full) name of the entity. For example, a dataset called 'Snow depth in the
    Northern Hemisphere' or a person called 'Sarah L. Jones' or a place called 'The Empire
    States Building'. Use unique names for distinct entities whenever possible.
    
    Identifier field of the data.
    
    Provider definition name.
    
    Time field of the data.
    
    Table name of the data.
    
    Geometry field of the data.
    
    X field name of the data.
    
    Y field name of the data.
    
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
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    
    Licensing and terms of use for the object, preferably as a URI with a description
    
    The technique, technology, or methodology used in a dataset, which can correspond to the
    variable(s) described in variableMeasured. The measurementTechnique property is proposed
    and pending standardization at schema.org, see
    https://pending.webschemas.org/measurementTechnique
    """
    PROPERTY_VALUE = "PropertyValue"


class PropertyValue:
    """Adaptation of schema.org PropertyValue for the description of the physical quantities of
    data variables (fields or parameters). Note this is non standard and includes extra
    properties from the CF standard name definition
    (http://cfconventions.org/cf-conventions/cf-conventions.html#standard-name).
    """
    type: PropertyValueType
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
    """Name of the property as used in the dataset."""
    name: str
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
    """Value of the property."""
    value: Union[List[Any], bool, float, int, Dict[str, Any], None, str]

    def __init__(self, type: PropertyValueType, canonical_units: Optional[str], description: Optional[str], long_name: Optional[str], name: str, same_as: Optional[str], standard_name: Optional[str], unit_text: Optional[str], value: Union[List[Any], bool, float, int, Dict[str, Any], None, str]) -> None:
        self.type = type
        self.canonical_units = canonical_units
        self.description = description
        self.long_name = long_name
        self.name = name
        self.same_as = same_as
        self.standard_name = standard_name
        self.unit_text = unit_text
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'PropertyValue':
        assert isinstance(obj, dict)
        type = PropertyValueType(obj.get("@type"))
        canonical_units = from_union([from_str, from_none], obj.get("canonical_units"))
        description = from_union([from_str, from_none], obj.get("description"))
        long_name = from_union([from_str, from_none], obj.get("long_name"))
        name = from_str(obj.get("name"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        standard_name = from_union([from_str, from_none], obj.get("standard_name"))
        unit_text = from_union([from_str, from_none], obj.get("unitText"))
        value = from_union([from_float, from_int, from_bool, lambda x: from_dict(lambda x: x, x), lambda x: from_list(lambda x: x, x), from_str, from_none], obj.get("value"))
        return PropertyValue(type, canonical_units, description, long_name, name, same_as, standard_name, unit_text, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(PropertyValueType, self.type)
        result["canonical_units"] = from_union([from_str, from_none], self.canonical_units)
        result["description"] = from_union([from_str, from_none], self.description)
        result["long_name"] = from_union([from_str, from_none], self.long_name)
        result["name"] = from_str(self.name)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["standard_name"] = from_union([from_str, from_none], self.standard_name)
        result["unitText"] = from_union([from_str, from_none], self.unit_text)
        result["value"] = from_union([to_float, from_int, from_bool, lambda x: from_dict(lambda x: x, x), lambda x: from_list(lambda x: x, x), from_str, from_none], self.value)
        return result


class Dataset:
    """A vizzToolsCore Dataset metadata/configuration object. This is an extended version of
    schema.org [Dataset](https://schema.org/Dataset) following the Google structured data
    Dataset guidelines. Non schema.org extensions to this include the properties;
    [dataProviders](https://vizztools.github.io/vizzToolsCore/json-schema/dataProviders).
    """
    schema: Optional[str]
    context: Optional[str]
    id: str
    type: Optional[DatasetType]
    alternate_name: Union[List[str], None, str]
    citation: Union[List[str], None, str]
    creator: Optional[List[SDPublisher]]
    data_providers: Optional[List[DataProvider]]
    date_created: Optional[datetime]
    date_modified: Optional[datetime]
    date_published: Optional[datetime]
    description: Optional[str]
    distribution: Optional[List[DataDownload]]
    funder: Optional[List[SDPublisher]]
    has_part: Optional[List[Union[Dict[str, Any], str]]]
    identifier: Union[List[str], None, str]
    in_language: Optional[InLanguage]
    is_based_on: Optional[str]
    is_part_of: Optional[List[Union[Dict[str, Any], str]]]
    license: Optional[str]
    measurement_technique: Optional[str]
    name: Optional[str]
    provider: Optional[List[SDPublisher]]
    same_as: Optional[str]
    sd_publisher: Optional[SDPublisher]
    spatial_coverage: Union[Place, None, str]
    temporal_coverage: Optional[str]
    thumbnail_url: Optional[str]
    url: Optional[str]
    variable_measured: Union[PropertyValue, None, str]
    version: Union[int, None, str]

    def __init__(self, schema: Optional[str], context: Optional[str], id: str, type: Optional[DatasetType], alternate_name: Union[List[str], None, str], citation: Union[List[str], None, str], creator: Optional[List[SDPublisher]], data_providers: Optional[List[DataProvider]], date_created: Optional[datetime], date_modified: Optional[datetime], date_published: Optional[datetime], description: Optional[str], distribution: Optional[List[DataDownload]], funder: Optional[List[SDPublisher]], has_part: Optional[List[Union[Dict[str, Any], str]]], identifier: Union[List[str], None, str], in_language: Optional[InLanguage], is_based_on: Optional[str], is_part_of: Optional[List[Union[Dict[str, Any], str]]], license: Optional[str], measurement_technique: Optional[str], name: Optional[str], provider: Optional[List[SDPublisher]], same_as: Optional[str], sd_publisher: Optional[SDPublisher], spatial_coverage: Union[Place, None, str], temporal_coverage: Optional[str], thumbnail_url: Optional[str], url: Optional[str], variable_measured: Union[PropertyValue, None, str], version: Union[int, None, str]) -> None:
        self.schema = schema
        self.context = context
        self.id = id
        self.type = type
        self.alternate_name = alternate_name
        self.citation = citation
        self.creator = creator
        self.data_providers = data_providers
        self.date_created = date_created
        self.date_modified = date_modified
        self.date_published = date_published
        self.description = description
        self.distribution = distribution
        self.funder = funder
        self.has_part = has_part
        self.identifier = identifier
        self.in_language = in_language
        self.is_based_on = is_based_on
        self.is_part_of = is_part_of
        self.license = license
        self.measurement_technique = measurement_technique
        self.name = name
        self.provider = provider
        self.same_as = same_as
        self.sd_publisher = sd_publisher
        self.spatial_coverage = spatial_coverage
        self.temporal_coverage = temporal_coverage
        self.thumbnail_url = thumbnail_url
        self.url = url
        self.variable_measured = variable_measured
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'Dataset':
        assert isinstance(obj, dict)
        schema = from_union([from_str, from_none], obj.get("$schema"))
        context = from_union([from_str, from_none], obj.get("@context"))
        id = from_str(obj.get("@id"))
        type = from_union([DatasetType, from_none], obj.get("@type"))
        alternate_name = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("alternateName"))
        citation = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("citation"))
        creator = from_union([lambda x: from_list(SDPublisher.from_dict, x), from_none], obj.get("creator"))
        data_providers = from_union([lambda x: from_list(DataProvider.from_dict, x), from_none], obj.get("dataProviders"))
        date_created = from_union([from_datetime, from_none], obj.get("dateCreated"))
        date_modified = from_union([from_datetime, from_none], obj.get("dateModified"))
        date_published = from_union([from_datetime, from_none], obj.get("datePublished"))
        description = from_union([from_str, from_none], obj.get("description"))
        distribution = from_union([lambda x: from_list(DataDownload.from_dict, x), from_none], obj.get("distribution"))
        funder = from_union([lambda x: from_list(SDPublisher.from_dict, x), from_none], obj.get("funder"))
        has_part = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], obj.get("hasPart"))
        identifier = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("identifier"))
        in_language = from_union([InLanguage, from_none], obj.get("inLanguage"))
        is_based_on = from_union([from_str, from_none], obj.get("isBasedOn"))
        is_part_of = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], obj.get("isPartOf"))
        license = from_union([from_str, from_none], obj.get("license"))
        measurement_technique = from_union([from_str, from_none], obj.get("measurementTechnique"))
        name = from_union([from_str, from_none], obj.get("name"))
        provider = from_union([lambda x: from_list(SDPublisher.from_dict, x), from_none], obj.get("provider"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        sd_publisher = from_union([SDPublisher.from_dict, from_none], obj.get("sdPublisher"))
        spatial_coverage = from_union([Place.from_dict, from_str, from_none], obj.get("spatialCoverage"))
        temporal_coverage = from_union([from_str, from_none], obj.get("temporalCoverage"))
        thumbnail_url = from_union([from_str, from_none], obj.get("thumbnailUrl"))
        url = from_union([from_str, from_none], obj.get("url"))
        variable_measured = from_union([PropertyValue.from_dict, from_str, from_none], obj.get("variableMeasured"))
        version = from_union([from_int, from_str, from_none], obj.get("version"))
        return Dataset(schema, context, id, type, alternate_name, citation, creator, data_providers, date_created, date_modified, date_published, description, distribution, funder, has_part, identifier, in_language, is_based_on, is_part_of, license, measurement_technique, name, provider, same_as, sd_publisher, spatial_coverage, temporal_coverage, thumbnail_url, url, variable_measured, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["$schema"] = from_union([from_str, from_none], self.schema)
        result["@context"] = from_union([from_str, from_none], self.context)
        result["@id"] = from_str(self.id)
        result["@type"] = from_union([lambda x: to_enum(DatasetType, x), from_none], self.type)
        result["alternateName"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.alternate_name)
        result["citation"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.citation)
        result["creator"] = from_union([lambda x: from_list(lambda x: to_class(SDPublisher, x), x), from_none], self.creator)
        result["dataProviders"] = from_union([lambda x: from_list(lambda x: to_class(DataProvider, x), x), from_none], self.data_providers)
        result["dateCreated"] = from_union([lambda x: x.isoformat(), from_none], self.date_created)
        result["dateModified"] = from_union([lambda x: x.isoformat(), from_none], self.date_modified)
        result["datePublished"] = from_union([lambda x: x.isoformat(), from_none], self.date_published)
        result["description"] = from_union([from_str, from_none], self.description)
        result["distribution"] = from_union([lambda x: from_list(lambda x: to_class(DataDownload, x), x), from_none], self.distribution)
        result["funder"] = from_union([lambda x: from_list(lambda x: to_class(SDPublisher, x), x), from_none], self.funder)
        result["hasPart"] = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], self.has_part)
        result["identifier"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.identifier)
        result["inLanguage"] = from_union([lambda x: to_enum(InLanguage, x), from_none], self.in_language)
        result["isBasedOn"] = from_union([from_str, from_none], self.is_based_on)
        result["isPartOf"] = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], self.is_part_of)
        result["license"] = from_union([from_str, from_none], self.license)
        result["measurementTechnique"] = from_union([from_str, from_none], self.measurement_technique)
        result["name"] = from_union([from_str, from_none], self.name)
        result["provider"] = from_union([lambda x: from_list(lambda x: to_class(SDPublisher, x), x), from_none], self.provider)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["sdPublisher"] = from_union([lambda x: to_class(SDPublisher, x), from_none], self.sd_publisher)
        result["spatialCoverage"] = from_union([lambda x: to_class(Place, x), from_str, from_none], self.spatial_coverage)
        result["temporalCoverage"] = from_union([from_str, from_none], self.temporal_coverage)
        result["thumbnailUrl"] = from_union([from_str, from_none], self.thumbnail_url)
        result["url"] = from_union([from_str, from_none], self.url)
        result["variableMeasured"] = from_union([lambda x: to_class(PropertyValue, x), from_str, from_none], self.variable_measured)
        result["version"] = from_union([from_int, from_str, from_none], self.version)
        return result


def dataset_from_dict(s: Any) -> Dataset:
    return Dataset.from_dict(s)


def dataset_to_dict(x: Dataset) -> Any:
    return to_class(Dataset, x)
