from sqlalchemy import String, Column, Boolean
from app.db import Base
from app.utils import helpers
from sqlalchemy.orm import relationship
from . import users


class Contact(users.User):
    __tablename__ = 'contacts'
    contacts = None
    user = relationship('users.User', back_populates='contacts', secondary='users.UserContact')

