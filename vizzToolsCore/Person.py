# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = person_from_dict(json.loads(json_string))

from enum import Enum
from typing import Optional, Any, Union, TypeVar, Type, cast


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


class ContactPointType(Enum):
    """Identifier string of this object.
    
    Type of this object.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    String representing a URI.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
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


class OrganizationType(Enum):
    """Identifier string of this object.
    
    Type of this object.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    String representing a URI.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
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


class PersonType(Enum):
    """Identifier string of this object.
    
    Type of this object.
    
    Use the sameAs property to indicate the most canonical URLs for the original in cases of
    the entity. For example this may be a link to the original metadata of a dataset,
    definition of a property, Person, Organization or Place.
    
    String representing a URI.
    
    A descriptive name. For example, 'Snow depth in the Northern Hemisphere'. Use unique
    names for distinct entities whenever possible.
    """
    PERSON = "Person"


class Person:
    """A person (alive, dead, undead, or fictional)."""
    id: Optional[str]
    type: PersonType
    affiliation: Union[Organization, None, str]
    family_name: Optional[str]
    given_name: Optional[str]
    name: str
    same_as: Optional[str]

    def __init__(self, id: Optional[str], type: PersonType, affiliation: Union[Organization, None, str], family_name: Optional[str], given_name: Optional[str], name: str, same_as: Optional[str]) -> None:
        self.id = id
        self.type = type
        self.affiliation = affiliation
        self.family_name = family_name
        self.given_name = given_name
        self.name = name
        self.same_as = same_as

    @staticmethod
    def from_dict(obj: Any) -> 'Person':
        assert isinstance(obj, dict)
        id = from_union([from_str, from_none], obj.get("@id"))
        type = PersonType(obj.get("@type"))
        affiliation = from_union([Organization.from_dict, from_str, from_none], obj.get("affiliation"))
        family_name = from_union([from_str, from_none], obj.get("familyName"))
        given_name = from_union([from_str, from_none], obj.get("givenName"))
        name = from_str(obj.get("name"))
        same_as = from_union([from_str, from_none], obj.get("sameAs"))
        return Person(id, type, affiliation, family_name, given_name, name, same_as)

    def to_dict(self) -> dict:
        result: dict = {}
        result["@id"] = from_union([from_str, from_none], self.id)
        result["@type"] = to_enum(PersonType, self.type)
        result["affiliation"] = from_union([lambda x: to_class(Organization, x), from_str, from_none], self.affiliation)
        result["familyName"] = from_union([from_str, from_none], self.family_name)
        result["givenName"] = from_union([from_str, from_none], self.given_name)
        result["name"] = from_str(self.name)
        result["sameAs"] = from_union([from_str, from_none], self.same_as)
        return result


def person_from_dict(s: Any) -> Person:
    return Person.from_dict(s)


def person_to_dict(x: Person) -> Any:
    return to_class(Person, x)