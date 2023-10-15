from pydantic import BaseModel
from pydantic.v1.dataclasses import dataclass
from fastapi import Form


class UserBase(BaseModel):
    username: str = Form(None)
