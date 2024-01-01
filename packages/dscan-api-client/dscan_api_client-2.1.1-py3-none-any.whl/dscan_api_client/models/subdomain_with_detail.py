import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.subdomain_detail import SubdomainDetail


T = TypeVar("T", bound="SubdomainWithDetail")


@_attrs_define
class SubdomainWithDetail:
    """
    Attributes:
        id (int):
        subdomaindetail (SubdomainDetail):
        name (str):
        created_at (Optional[datetime.datetime]):
        updated_at (Optional[datetime.datetime]):
        enabled (Union[Unset, bool]):
        program (Union[Unset, None, int]):
    """

    id: int
    subdomaindetail: "SubdomainDetail"
    name: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    enabled: Union[Unset, bool] = UNSET
    program: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        subdomaindetail = self.subdomaindetail.to_dict()

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
                "subdomaindetail": subdomaindetail,
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
        from ..models.subdomain_detail import SubdomainDetail

        d = src_dict.copy()
        id = d.pop("id")

        subdomaindetail = SubdomainDetail.from_dict(d.pop("subdomaindetail"))

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

        subdomain_with_detail = cls(
            id=id,
            subdomaindetail=subdomaindetail,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            enabled=enabled,
            program=program,
        )

        subdomain_with_detail.additional_properties = d
        return subdomain_with_detail

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
