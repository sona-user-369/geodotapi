import uuid

from sqlalchemy import String, Column, Boolean, Table, ForeignKey, Text, Integer
from app.db import Base
from app.utils import helpers
from sqlalchemy.orm import relationship
from . import contacts


class User(Base):
    __tablename__ = 'users'

    id = Column(helpers.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    username = Column(String(60), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    con_id = Column(String(40), nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)
    contacts = relationship('Contact', back_populates='users', secondary='user_contacts')
    contact = relationship('Contact', back_populates="user")
    token = relationship('Token', back_populates='user')

    def __init__(self, username, con_id, password):
        self.username = username
        self.con_id = con_id
        self.password = password

    def update(self, data):
        self.username = data.username
        self.con_id = data.con_id


class UserContact(Base):
    __tablename__ = 'user_contacts'
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    contact_id = Column(ForeignKey('contacts.id'), primary_key=True)
    enable = Column(Boolean, default=False, nullable=False)

    def __init__(self, user_id, contact_id):
        self.user_id = user_id
        self.contact_id = contact_id

    def set_enable(self, value):
        self.enable = value


class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'),)
    user = relationship('User', back_populates='token')
    key = Column(Text, nullable=False,)

    def __init__(self, user_id, key):
        self.user_id = user_id
        self.key = key
