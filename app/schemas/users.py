from pydantic import BaseModel
from pydantic.v1.dataclasses import dataclass
from fastapi import Form
from typing import List
from . import contacts


@dataclass
class UserSchemeBase:
    username: str = Form(None)


@dataclass
class UserSchemeCreate(UserSchemeBase):
    password: str = Form(None)


@dataclass
class UserScheme(UserSchemeBase):
    id: str
    active: str
    contacts: List[contacts.ContactScheme]



