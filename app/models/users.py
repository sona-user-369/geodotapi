from sqlalchemy import String, Column, Boolean
from app.db import Base
from app.utils import helpers
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(helpers.UUID, primary_key=True, nullable=False)
    username = Column(String(60), nullable=False, unique=True)
    con_id = Column(String(40),  nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)
    contacts = relationship('Contact', back_populates='user_id', secondary='UserContact')


class UserContact(Base):
    __tablename__ = 'user_contacts'

    user_id = relationship('User', back_populates='contacts')
    match_id = relationship('Contact', back_populates='')
