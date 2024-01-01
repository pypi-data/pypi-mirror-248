import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.scan_status import ScanStatus
from ..models.scan_type_n import ScanTypeN
from ..models.scan_type_s import ScanTypeS
from ..types import UNSET, Unset

T = TypeVar("T", bound="Scan")


@_attrs_define
class Scan:
    """
    Attributes:
        id (int):
        name (str):
        status (Union[Unset, ScanStatus]): * `0` - Just Added - Will be Scheduled Soon
            * `1` - Scheduled/Started Enum Phase
            * `2` - Preparing data for HTTPX
            * `3` - Ready for HTTPX
            * `4` - HTTPX Started/Ongoing
            * `5` - Preparing data for Nuclei
            * `6` - Ready for Nuclei
            * `7` - Nuclei Started
            * `8` - Scan Finished
        issues_found (Union[Unset, None, int]):
        comment (Union[Unset, None, str]):
        created_at (Optional[datetime.datetime]):
        updated_at (Optional[datetime.datetime]):
        reason (Union[Unset, None, str]):
        s_type (Union[Unset, ScanTypeS]): * `0` - enum
            * `1` - httpx
            * `2` - enumx
            * `3` - nuclei
            * `4` - full
        n_type (Union[Unset, ScanTypeN]): * `0` - local
            * `1` - full
            * `2` - new
        program (Union[Unset, None, int]):
        e_type (Union[Unset, None, int]):
    """

    id: int
    name: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    status: Union[Unset, ScanStatus] = UNSET
    issues_found: Union[Unset, None, int] = UNSET
    comment: Union[Unset, None, str] = UNSET
    reason: Union[Unset, None, str] = UNSET
    s_type: Union[Unset, ScanTypeS] = UNSET
    n_type: Union[Unset, ScanTypeN] = UNSET
    program: Union[Unset, None, int] = UNSET
    e_type: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        issues_found = self.issues_found
        comment = self.comment
        created_at = self.created_at.isoformat() if self.created_at else None

        updated_at = self.updated_at.isoformat() if self.updated_at else None

        reason = self.reason
        s_type: Union[Unset, int] = UNSET
        if not isinstance(self.s_type, Unset):
            s_type = self.s_type.value

        n_type: Union[Unset, int] = UNSET
        if not isinstance(self.n_type, Unset):
            n_type = self.n_type.value

        program = self.program
        e_type = self.e_type

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
        if status is not UNSET:
            field_dict["status"] = status
        if issues_found is not UNSET:
            field_dict["issues_found"] = issues_found
        if comment is not UNSET:
            field_dict["comment"] = comment
        if reason is not UNSET:
            field_dict["reason"] = reason
        if s_type is not UNSET:
            field_dict["s_type"] = s_type
        if n_type is not UNSET:
            field_dict["n_type"] = n_type
        if program is not UNSET:
            field_dict["program"] = program
        if e_type is not UNSET:
            field_dict["e_type"] = e_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        _status = d.pop("status", UNSET)
        status: Union[Unset, ScanStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ScanStatus(_status)

        issues_found = d.pop("issues_found", UNSET)

        comment = d.pop("comment", UNSET)

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

        reason = d.pop("reason", UNSET)

        _s_type = d.pop("s_type", UNSET)
        s_type: Union[Unset, ScanTypeS]
        if isinstance(_s_type, Unset):
            s_type = UNSET
        else:
            s_type = ScanTypeS(_s_type)

        _n_type = d.pop("n_type", UNSET)
        n_type: Union[Unset, ScanTypeN]
        if isinstance(_n_type, Unset):
            n_type = UNSET
        else:
            n_type = ScanTypeN(_n_type)

        program = d.pop("program", UNSET)

        e_type = d.pop("e_type", UNSET)

        scan = cls(
            id=id,
            name=name,
            status=status,
            issues_found=issues_found,
            comment=comment,
            created_at=created_at,
            updated_at=updated_at,
            reason=reason,
            s_type=s_type,
            n_type=n_type,
            program=program,
            e_type=e_type,
        )

        scan.additional_properties = d
        return scan

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
