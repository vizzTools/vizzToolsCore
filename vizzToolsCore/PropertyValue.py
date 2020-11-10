# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = property_value_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, List, Any, Dict, Union, TypeVar, Callable, Type, cast


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


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


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
    """Type of this object.
    
    Use the sameAs property to indicate the most canonical URL for the original description
    of the property.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    String representing a URI.
    
    A string or text indicating the actual unit of measurement (which maybe different to the
    canonical_units). In general this should be of the form 'm / s', leave a space between
    each character. Use SI prefix symbols; https://en.wikipedia.org/wiki/Metric_prefix.
    Dimensionless units are indicated by '1'.
    """
    PROPERTY_VALUE = "PropertyValue"


class PropertyValue:
    """Adaptation of schema.org PropertyValue for the description of the physical quantities of
    data variables (fields or parameters). Note this is non standard and includes extra
    properties from the CF standard name definition
    (http://cfconventions.org/cf-conventions/cf-conventions.html#standard-name).
    """
    type: TypeEnum
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

    def __init__(self, type: TypeEnum, canonical_units: Optional[str], description: Optional[str], long_name: Optional[str], name: str, same_as: Optional[str], standard_name: Optional[str], unit_text: Optional[str], value: Union[List[Any], bool, float, int, Dict[str, Any], None, str]) -> None:
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
        type = TypeEnum(obj.get("@type"))
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
        result["@type"] = to_enum(TypeEnum, self.type)
        result["canonical_units"] = from_union([from_str, from_none], self.canonical_units)
        result["description"] = from_union([from_str, from_none], self.description)
        result["long_name"] = from_union([from_str, from_none], self.long_name)
        result["name"] = from_str(self.name)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        result["standard_name"] = from_union([from_str, from_none], self.standard_name)
        result["unitText"] = from_union([from_str, from_none], self.unit_text)
        result["value"] = from_union([to_float, from_int, from_bool, lambda x: from_dict(lambda x: x, x), lambda x: from_list(lambda x: x, x), from_str, from_none], self.value)
        return result


def property_value_from_dict(s: Any) -> PropertyValue:
    return PropertyValue.from_dict(s)


def property_value_to_dict(x: PropertyValue) -> Any:
    return to_class(PropertyValue, x)
