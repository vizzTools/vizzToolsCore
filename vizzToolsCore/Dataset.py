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
from typing import Optional, Any, List, Dict, Union, TypeVar, Type, cast, Callable
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


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


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
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
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
    CONTACT_POINT = "contactPoint"


class ContactPoint:
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


class AffiliationType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
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
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
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
    type: AffiliationType
    contact_point: Optional[ContactPoint]
    name: str
    same_as: Optional[str]
    url: Optional[str]

    def __init__(self, id: Optional[str], type: AffiliationType, contact_point: Optional[ContactPoint], name: str, same_as: Optional[str], url: Optional[str]) -> None:
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
        type = AffiliationType(obj.get("@type"))
        contact_point = from_union([ContactPoint.from_dict, from_none], obj.get("contactPoint"))
        name = from_str(obj.get("name"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Organization(id, type, contact_point, name, same_as, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@id"] = from_union([from_str, from_none], self.id)
        result["@type"] = to_enum(AffiliationType, self.type)
        result["contactPoint"] = from_union([lambda x: to_class(ContactPoint, x), from_none], self.contact_point)
        result["name"] = from_str(self.name)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class CreatorType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
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
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
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


class Creator:
    """An array of schema.org Person or Organization objects. To uniquely identify individuals,
    use ORCID ID as the value of the sameAs property of the Person type. To uniquely identify
    institutions and organizations, use ROR ID.
    
    A person (alive, dead, undead, or fictional).
    
    An organization such as a school, NGO, corporation, club, etc.
    """
    id: Optional[str]
    type: CreatorType
    affiliation: Optional[Organization]
    family_name: Optional[str]
    given_name: Optional[str]
    name: str
    same_as: Optional[str]
    contact_point: Optional[ContactPoint]
    url: Optional[str]

    def __init__(self, id: Optional[str], type: CreatorType, affiliation: Optional[Organization], family_name: Optional[str], given_name: Optional[str], name: str, same_as: Optional[str], contact_point: Optional[ContactPoint], url: Optional[str]) -> None:
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
    def from_dict(obj: Any) -> 'Creator':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("@id"))
        type = CreatorType(obj.get("@type"))
        affiliation = from_union([Organization.from_dict, from_none], obj.get("affiliation"))
        family_name = from_union([from_str, from_none], obj.get("familyName"))
        given_name = from_union([from_str, from_none], obj.get("givenName"))
        name = from_str(obj.get("name"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        contact_point = from_union([ContactPoint.from_dict, from_none], obj.get("contactPoint"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Creator(id, type, affiliation, family_name, given_name, name, same_as, contact_point, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@id"] = from_union([from_str, from_none], self.id)
        result["@type"] = to_enum(CreatorType, self.type)
        result["affiliation"] = from_union([lambda x: to_class(Organization, x), from_none], self.affiliation)
        result["familyName"] = from_union([from_str, from_none], self.family_name)
        result["givenName"] = from_union([from_str, from_none], self.given_name)
        result["name"] = from_str(self.name)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["contactPoint"] = from_union([lambda x: to_class(ContactPoint, x), from_none], self.contact_point)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


class DataDownload:
    """An array of schema.org DataDownload objects that describe URIs to access to the entity.
    
    A schema.org DataDownload object representing the location and file format for
    downloadable data.
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
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
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
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
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


class DatasetType(Enum):
    """URI of the JSON schema of this object.
    
    String representing a URI.
    
    A URL that provides descriptions of this objects properties. TODO: Align with full
    JSON-LD context definition!
    
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
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
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
    
    Identifier string of this object.
    
    Type of this object.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    
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
    """A schema.org Dataset metadata object that describes the dataset."""
    schema: str
    context: str
    id: Optional[str]
    type: DatasetType
    alternate_name: Union[List[str], None, str]
    citation: Union[List[str], None, str]
    creator: Optional[List[Creator]]
    date_published: Optional[datetime]
    description: str
    distribution: Optional[List[DataDownload]]
    funder: Optional[List[Creator]]
    has_part: Optional[List[Union[Dict[str, Any], str]]]
    identifier: Union[List[str], None, str]
    in_language: Optional[InLanguage]
    is_based_on: Optional[str]
    is_part_of: Optional[List[Union[Dict[str, Any], str]]]
    license: Optional[str]
    measurement_technique: Optional[str]
    name: str
    provider: Optional[List[Creator]]
    """Use the sameAs property to indicate the most canonical URLs for the original in cases
    when the dataset or description is a simple republication of materials published
    elsewhere. The value of sameAs needs to unambiguously indicate the datasets identity - in
    other words two different datasets should not use the same URL as sameAs value.
    """
    same_as: Optional[str]
    spatial_coverage: Union[Place, None, str]
    temporal_coverage: Optional[str]
    thumbnail_url: Optional[str]
    url: Optional[str]
    variable_measured: Union[PropertyValue, None, str]
    version: Union[int, None, str]

    def __init__(self, schema: str, context: str, id: Optional[str], type: DatasetType, alternate_name: Union[List[str], None, str], citation: Union[List[str], None, str], creator: Optional[List[Creator]], date_published: Optional[datetime], description: str, distribution: Optional[List[DataDownload]], funder: Optional[List[Creator]], has_part: Optional[List[Union[Dict[str, Any], str]]], identifier: Union[List[str], None, str], in_language: Optional[InLanguage], is_based_on: Optional[str], is_part_of: Optional[List[Union[Dict[str, Any], str]]], license: Optional[str], measurement_technique: Optional[str], name: str, provider: Optional[List[Creator]], same_as: Optional[str], spatial_coverage: Union[Place, None, str], temporal_coverage: Optional[str], thumbnail_url: Optional[str], url: Optional[str], variable_measured: Union[PropertyValue, None, str], version: Union[int, None, str]) -> None:
        self.schema = schema
        self.context = context
        self.id = id
        self.type = type
        self.alternate_name = alternate_name
        self.citation = citation
        self.creator = creator
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
        self.spatial_coverage = spatial_coverage
        self.temporal_coverage = temporal_coverage
        self.thumbnail_url = thumbnail_url
        self.url = url
        self.variable_measured = variable_measured
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'Dataset':
        assert isinstance(obj, dict)
        schema = from_str(obj.get("$schema"))
        context = from_str(obj.get("@context"))
        id = from_union([from_str, from_none], obj.get("@id"))
        type = DatasetType(obj.get("@type"))
        alternate_name = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("alternateName"))
        citation = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("citation"))
        creator = from_union([lambda x: from_list(Creator.from_dict, x), from_none], obj.get("creator"))
        date_published = from_union([from_datetime, from_none], obj.get("datePublished"))
        description = from_str(obj.get("description"))
        distribution = from_union([lambda x: from_list(DataDownload.from_dict, x), from_none], obj.get("distribution"))
        funder = from_union([lambda x: from_list(Creator.from_dict, x), from_none], obj.get("funder"))
        has_part = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], obj.get("hasPart"))
        identifier = from_union([lambda x: from_list(from_str, x), from_str, from_none], obj.get("identifier"))
        in_language = from_union([InLanguage, from_none], obj.get("inLanguage"))
        is_based_on = from_union([from_str, from_none], obj.get("isBasedOn"))
        is_part_of = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], obj.get("isPartOf"))
        license = from_union([from_str, from_none], obj.get("license"))
        measurement_technique = from_union([from_str, from_none], obj.get("measurementTechnique"))
        name = from_str(obj.get("name"))
        provider = from_union([lambda x: from_list(Creator.from_dict, x), from_none], obj.get("provider"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        spatial_coverage = from_union([Place.from_dict, from_str, from_none], obj.get("spatialCoverage"))
        temporal_coverage = from_union([from_str, from_none], obj.get("temporalCoverage"))
        thumbnail_url = from_union([from_str, from_none], obj.get("thumbnailUrl"))
        url = from_union([from_str, from_none], obj.get("url"))
        variable_measured = from_union([PropertyValue.from_dict, from_str, from_none], obj.get("variableMeasured"))
        version = from_union([from_int, from_str, from_none], obj.get("version"))
        return Dataset(schema, context, id, type, alternate_name, citation, creator, date_published, description, distribution, funder, has_part, identifier, in_language, is_based_on, is_part_of, license, measurement_technique, name, provider, same_as, spatial_coverage, temporal_coverage, thumbnail_url, url, variable_measured, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["$schema"] = from_str(self.schema)
        result["@context"] = from_str(self.context)
        result["@id"] = from_union([from_str, from_none], self.id)
        result["@type"] = to_enum(DatasetType, self.type)
        result["alternateName"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.alternate_name)
        result["citation"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.citation)
        result["creator"] = from_union([lambda x: from_list(lambda x: to_class(Creator, x), x), from_none], self.creator)
        result["datePublished"] = from_union([lambda x: x.isoformat(), from_none], self.date_published)
        result["description"] = from_str(self.description)
        result["distribution"] = from_union([lambda x: from_list(lambda x: to_class(DataDownload, x), x), from_none], self.distribution)
        result["funder"] = from_union([lambda x: from_list(lambda x: to_class(Creator, x), x), from_none], self.funder)
        result["hasPart"] = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], self.has_part)
        result["identifier"] = from_union([lambda x: from_list(from_str, x), from_str, from_none], self.identifier)
        result["inLanguage"] = from_union([lambda x: to_enum(InLanguage, x), from_none], self.in_language)
        result["isBasedOn"] = from_union([from_str, from_none], self.is_based_on)
        result["isPartOf"] = from_union([lambda x: from_list(lambda x: from_union([lambda x: from_dict(lambda x: x, x), from_str], x), x), from_none], self.is_part_of)
        result["license"] = from_union([from_str, from_none], self.license)
        result["measurementTechnique"] = from_union([from_str, from_none], self.measurement_technique)
        result["name"] = from_str(self.name)
        result["provider"] = from_union([lambda x: from_list(lambda x: to_class(Creator, x), x), from_none], self.provider)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
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
