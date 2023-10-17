import uuid

from pydantic import BaseModel
from pydantic.v1.dataclasses import dataclass
from fastapi import Form
from typing import List
from . import users


@dataclass
class ContactSchemeBase:
    id: uuid.UUID = Form(None)


@dataclass
class ContactScheme(ContactSchemeBase):
    user = users.UserSchemeBase


