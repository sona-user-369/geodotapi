import uuid

from sqlalchemy import String, Column, Boolean, Table, ForeignKey
from app.db import Base
from app.utils import helpers
from sqlalchemy.orm import relationship
from . import contacts


class User(Base):
    __tablename__ = 'users'

    id = Column(helpers.UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    username = Column(String(60), nullable=False, unique=True)
    con_id = Column(String(40),  nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)
    contacts = relationship('Contact', back_populates='users', secondary='user_contacts')

    def __init__(self, username, con_id):
        self.username = username
        self.con_id = con_id

    def update(self, data):
        self.username = data.username
        self.con_id = data.con_id


user_contact = Table(
    "user_contacts",
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('contact_id', ForeignKey('contacts.id'), primary_key=True),
)
