from uuid import UUID
from pydantic import BaseModel
from typing import List, Literal
from .device import Display


class Traits(BaseModel):
    extraversion: int
    agreeableness: int
    openness: int
    conscientiousness: int
    neuroticism: int


class Behavior(BaseModel):
    name: str
    description: str


class Character(BaseModel):
    name: str
    personality: str
    traits: Traits
    behaviors: List[Behavior] = []
    voice: Display | None = None


class Pet(BaseModel):
    uuid: UUID | None = None
    user: UUID
    device: UUID
    icon_image_name: str | None = None
    assistant_id: str | None = None
    model: Literal["gpt-3.5-turbo-1106", "gpt-4-1106-preview"]
    character: Character
