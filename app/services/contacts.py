import uuid
from typing import List

from sqlalchemy.orm import Session
from app.models.users import User, UserContact
from app.models.contacts import Contact
from fastapi import HTTPException, status
from ..utils.helpers import cache


async def get_contact(contact_id, db):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        contact = Contact(user_id=contact_id)
        db.add(contact)
        db.commit()
        db.refresh(contact)
    return contact


async def get_contacts(user_id: uuid.UUID, db: Session) -> List:
    user = db.query(User).filter(User.id == user_id)
    # contacts = db.query(Contact).filter(Contact)
    user_contact: List[UserContact] = db.query(UserContact).filter(UserContact.user_id == user_id).all()
    contacts = list(map(lambda x:
                        {
                            "id": x.contact_id,
                            "user": user,
                            "state": x,
                            "online": True if cache.get(str(x.contact_id)) else False
                        }
                        , user_contact))

    return contacts


async def verify_contact(con_id, db):
    user = db.query(User).filter(User.con_id == con_id).first()
    if not user:
        raise HTTPException(
            detail='This user is not found',
            status_code=status.HTTP_404_NOT_FOUND
        )
    return user


async def add_contact(con_id, user_id, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    contact_user = await verify_contact(con_id, db)
    contact = await get_contact(contact_id=contact_user.id, db=db)
    if contact in user.contacts:
        raise HTTPException(
            detail='This user is already contact of this one user',
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    user_contact = UserContact(user_id, contact.id)
    db.add(user_contact)
    db.commit()
    db.refresh(user)

    return user


async def confirm_match(user_id, contact_id, db: Session):
    user_contact: UserContact = db.query(UserContact).filter(UserContact.user_id == user_id,
                                                             UserContact.contact_id == contact_id)
    user_contact.set_enable(True)
    db.commit()
    db.refresh(user_contact)
