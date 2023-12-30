from uuid import UUID
from pydantic import BaseModel
from typing import Dict, List, Literal


class FunctionProperty(BaseModel):
    type: Literal["string", "int", "float"]
    enum: List[str] | None = None


class FunctionParameters(BaseModel):
    type: str = "object"
    properties: Dict[str, FunctionProperty]


class Function(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters


class Display(BaseModel):
    name: str
    args: Dict[str, str] | None = None


class Skeleton(BaseModel):
    displays: List[Display]
    functions: List[Function] = []


class Device(BaseModel):
    uuid: UUID | None = None
    tag: str
    skeleton: Skeleton
