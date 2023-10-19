import uuid

from pydantic import BaseModel, ConfigDict, field_validator, validator
from pydantic.v1.dataclasses import dataclass
from fastapi import Form
from typing import List, Union
from app import db
from app.models import  users


@dataclass
class UserSchemeBase:
    username: str = Form()


@dataclass
class UserSchemeCreate(UserSchemeBase):
    password: str = Form()

    @validator('username', pre=True, always=True)
    def validate_username(cls, value):
        print(value)
        database = db.get_db()
        for d in database:
            database = d
        user = database.query(users.User).filter(users.User.username == value).first()
        if user:
            raise ValueError('user with this username already exist')
        print(value)
        return value


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
