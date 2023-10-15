from pydantic.typing import String
from app.db import Base


class User(BaseModel):
    __tablename__ = 'users'

    id = String()
