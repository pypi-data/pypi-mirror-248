import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.scanner_type import ScannerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedScanner")


@_attrs_define
class PatchedScanner:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        s_type (Union[Unset, ScannerType]): * `0` - k8s
            * `1` - enumerator
            * `2` - httpx
            * `3` - nuclei
        config (Union[Unset, None, str]):
        enabled (Union[Unset, bool]):
        comment (Union[Unset, None, str]):
        created_at (Union[Unset, None, datetime.datetime]):
        updated_at (Union[Unset, None, datetime.datetime]):
        version (Union[Unset, None, str]):
        commit (Union[Unset, None, str]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    s_type: Union[Unset, ScannerType] = UNSET
    config: Union[Unset, None, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    comment: Union[Unset, None, str] = UNSET
    created_at: Union[Unset, None, datetime.datetime] = UNSET
    updated_at: Union[Unset, None, datetime.datetime] = UNSET
    version: Union[Unset, None, str] = UNSET
    commit: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        s_type: Union[Unset, int] = UNSET
        if not isinstance(self.s_type, Unset):
            s_type = self.s_type.value

        config = self.config
        enabled = self.enabled
        comment = self.comment
        created_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat() if self.created_at else None

        updated_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat() if self.updated_at else None

        version = self.version
        commit = self.commit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if s_type is not UNSET:
            field_dict["s_type"] = s_type
        if config is not UNSET:
            field_dict["config"] = config
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if comment is not UNSET:
            field_dict["comment"] = comment
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if version is not UNSET:
            field_dict["version"] = version
        if commit is not UNSET:
            field_dict["commit"] = commit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _s_type = d.pop("s_type", UNSET)
        s_type: Union[Unset, ScannerType]
        if isinstance(_s_type, Unset):
            s_type = UNSET
        else:
            s_type = ScannerType(_s_type)

        config = d.pop("config", UNSET)

        enabled = d.pop("enabled", UNSET)

        comment = d.pop("comment", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, None, datetime.datetime]
        if _created_at is None:
            created_at = None
        elif isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, None, datetime.datetime]
        if _updated_at is None:
            updated_at = None
        elif isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        version = d.pop("version", UNSET)

        commit = d.pop("commit", UNSET)

        patched_scanner = cls(
            id=id,
            name=name,
            s_type=s_type,
            config=config,
            enabled=enabled,
            comment=comment,
            created_at=created_at,
            updated_at=updated_at,
            version=version,
            commit=commit,
        )

        patched_scanner.additional_properties = d
        return patched_scanner

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
