import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.task_status import TaskStatus
from ..models.task_type import TaskType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedTask")


@_attrs_define
class PatchedTask:
    """
    Attributes:
        id (Union[Unset, int]):
        task_id (Union[Unset, str]):
        status (Union[Unset, TaskStatus]): * `0` - Queued
            * `1` - Started
            * `2` - Retry
            * `3` - Failure
            * `9` - Success
            * `10` - Forced
        is_finished (Union[Unset, None, bool]):
        created_at (Union[Unset, None, datetime.datetime]):
        updated_at (Union[Unset, None, datetime.datetime]):
        task_type (Union[Unset, TaskType]): * `0` - assetfinder
            * `1` - amass
            * `2` - subfinder
            * `3` - httpx
            * `4` - nuclei
        scan (Union[Unset, None, int]):
    """

    id: Union[Unset, int] = UNSET
    task_id: Union[Unset, str] = UNSET
    status: Union[Unset, TaskStatus] = UNSET
    is_finished: Union[Unset, None, bool] = UNSET
    created_at: Union[Unset, None, datetime.datetime] = UNSET
    updated_at: Union[Unset, None, datetime.datetime] = UNSET
    task_type: Union[Unset, TaskType] = UNSET
    scan: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        task_id = self.task_id
        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        is_finished = self.is_finished
        created_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat() if self.created_at else None

        updated_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat() if self.updated_at else None

        task_type: Union[Unset, int] = UNSET
        if not isinstance(self.task_type, Unset):
            task_type = self.task_type.value

        scan = self.scan

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if status is not UNSET:
            field_dict["status"] = status
        if is_finished is not UNSET:
            field_dict["is_finished"] = is_finished
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if task_type is not UNSET:
            field_dict["task_type"] = task_type
        if scan is not UNSET:
            field_dict["scan"] = scan

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        task_id = d.pop("task_id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, TaskStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = TaskStatus(_status)

        is_finished = d.pop("is_finished", UNSET)

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

        _task_type = d.pop("task_type", UNSET)
        task_type: Union[Unset, TaskType]
        if isinstance(_task_type, Unset):
            task_type = UNSET
        else:
            task_type = TaskType(_task_type)

        scan = d.pop("scan", UNSET)

        patched_task = cls(
            id=id,
            task_id=task_id,
            status=status,
            is_finished=is_finished,
            created_at=created_at,
            updated_at=updated_at,
            task_type=task_type,
            scan=scan,
        )

        patched_task.additional_properties = d
        return patched_task

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
