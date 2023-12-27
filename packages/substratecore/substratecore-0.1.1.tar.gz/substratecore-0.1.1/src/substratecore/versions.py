from .pydantic_models import ErrorOut
from typing import Dict, Any, TypeVar, Generic, Union
from pydantic import BaseModel
from abc import ABC, abstractmethod

M = TypeVar("M", bound=BaseModel, covariant=True)


class ToIn(Generic[M], ABC):
    def __init__(self, json: Dict[str, Any]):
        self.json = json

    @abstractmethod
    def from_version(self, version: str) -> Union[M, ErrorOut]:
        """
        Translate a JSON request from a past version to the current model shape.
        """
        raise NotImplementedError()


class FromOut(Generic[M], ABC):
    def __init__(self, model: M):
        self.model = model

    @abstractmethod
    def to_version(self, version: str) -> Dict[str, Any]:
        """
        Translate a response in the current model shape to a past version.
        """
        raise NotImplementedError()
