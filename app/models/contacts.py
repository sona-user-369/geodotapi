from sqlalchemy import String, Column, Boolean, ForeignKey
from app.db import Base
from app.utils import helpers
from sqlalchemy.orm import relationship
from . import users


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(ForeignKey("users.id", ondelete='NO ACTION'), primary_key=True)
    users = relationship('User', back_populates='contacts', secondary='user_contacts')
    user = relationship('User', back_populates="contact")

    def __init__(self, user_id):
        self.id = user_id

