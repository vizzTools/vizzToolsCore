# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = contact_point_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, Any, TypeVar, Type, cast


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


class TypeEnum(Enum):
    """Type of this object."""
    CONTACT_POINT = "ContactPoint"


class ContactPoint:
    """A contact point—for example, a Customer Complaints department."""
    type: TypeEnum
    contact_type: Optional[str]
    email: str
    telephone: Optional[str]

    def __init__(self, type: TypeEnum, contact_type: Optional[str], email: str, telephone: Optional[str]) -> None:
        self.type = type
        self.contact_type = contact_type
        self.email = email
        self.telephone = telephone

    @staticmethod
    def from_dict(obj: Any) -> 'ContactPoint':
        assert isinstance(obj, dict)
        type = TypeEnum(obj.get("@type"))
        contact_type = from_union([from_str, from_none], obj.get("contactType"))
        email = from_str(obj.get("email"))
        telephone = from_union([from_str, from_none], obj.get("telephone"))
        return ContactPoint(type, contact_type, email, telephone)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@type"] = to_enum(TypeEnum, self.type)
        result["contactType"] = from_union([from_str, from_none], self.contact_type)
        result["email"] = from_str(self.email)
        result["telephone"] = from_union([from_str, from_none], self.telephone)
        return result


def contact_point_from_dict(s: Any) -> ContactPoint:
    return ContactPoint.from_dict(s)


def contact_point_to_dict(x: ContactPoint) -> Any:
    return to_class(ContactPoint, x)