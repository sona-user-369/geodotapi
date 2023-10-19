import uuid

from pydantic import BaseModel, ConfigDict
from pydantic.v1.dataclasses import dataclass
from fastapi import Form
from typing import List, Union


@dataclass
class UserSchemeBase:
    username: str = Form()


@dataclass
class UserSchemeCreate(UserSchemeBase):
    password: str = Form()


class UserSchemeFree(BaseModel):
    username: str
    active: bool


class ContactScheme(BaseModel):
    id: uuid.UUID
    user: UserSchemeFree
    model_config = ConfigDict(from_attributes=True)


class UserScheme(BaseModel):
    id: uuid.UUID
    username: str
    active: bool
    contacts: List[ContactScheme] = None
    model_config = ConfigDict(from_attributes=True)


@dataclass
class Auth:
    username: str = Form()
    password: str = Form()


class TokenScheme(BaseModel):
    token: str
    type: str
    user: UserScheme
    model_config = ConfigDict(from_attributes=True)
