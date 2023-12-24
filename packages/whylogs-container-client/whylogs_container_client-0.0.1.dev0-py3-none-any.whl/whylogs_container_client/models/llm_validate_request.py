from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LLMValidateRequest")


@_attrs_define
class LLMValidateRequest:
    """
    Attributes:
        prompt (str):
        response (str):
        dataset_id (Union[Unset, str]):
        timestamp (Union[None, Unset, int]):
    """

    prompt: str
    response: str
    dataset_id: Union[Unset, str] = UNSET
    timestamp: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prompt = self.prompt
        response = self.response
        dataset_id = self.dataset_id
        timestamp: Union[None, Unset, int]
        if isinstance(self.timestamp, Unset):
            timestamp = UNSET

        else:
            timestamp = self.timestamp

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
                "response": response,
            }
        )
        if dataset_id is not UNSET:
            field_dict["datasetId"] = dataset_id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        response = d.pop("response")

        dataset_id = d.pop("datasetId", UNSET)

        def _parse_timestamp(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        timestamp = _parse_timestamp(d.pop("timestamp", UNSET))

        llm_validate_request = cls(
            prompt=prompt,
            response=response,
            dataset_id=dataset_id,
            timestamp=timestamp,
        )

        llm_validate_request.additional_properties = d
        return llm_validate_request

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
