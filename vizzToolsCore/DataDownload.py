# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = data_download_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class DataDownload:
    """A schema.org DataDownload object representing the location and file format for
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


def data_download_from_dict(s: Any) -> DataDownload:
    return DataDownload.from_dict(s)


def data_download_to_dict(x: DataDownload) -> Any:
    return to_class(DataDownload, x)
