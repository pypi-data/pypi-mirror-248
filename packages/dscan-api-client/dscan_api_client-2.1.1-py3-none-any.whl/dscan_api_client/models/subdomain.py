import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Subdomain")


@_attrs_define
class Subdomain:
    """
    Attributes:
        id (int):
        name (str):
        created_at (Optional[datetime.datetime]):
        updated_at (Optional[datetime.datetime]):
        enabled (Union[Unset, bool]):
        program (Union[Unset, None, int]):
    """

    id: int
    name: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    enabled: Union[Unset, bool] = UNSET
    program: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        created_at = self.created_at.isoformat() if self.created_at else None

        updated_at = self.updated_at.isoformat() if self.updated_at else None

        enabled = self.enabled
        program = self.program

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if program is not UNSET:
            field_dict["program"] = program

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        _created_at = d.pop("created_at")
        created_at: Optional[datetime.datetime]
        if _created_at is None:
            created_at = None
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at")
        updated_at: Optional[datetime.datetime]
        if _updated_at is None:
            updated_at = None
        else:
            updated_at = isoparse(_updated_at)

        enabled = d.pop("enabled", UNSET)

        program = d.pop("program", UNSET)

        subdomain = cls(
            id=id,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            enabled=enabled,
            program=program,
        )

        subdomain.additional_properties = d
        return subdomain

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
