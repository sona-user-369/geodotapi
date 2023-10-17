import random
import string
from sqlalchemy.orm import Session
from app.models.users import User
from app.models.contacts import Contact
from fastapi import HTTPException, status


async def generate_con_id():
    generated_key = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    generated_id = 'con{0}up'.format(generated_key)
    return generated_id


async def register_user(user, db: Session):
    user_object = User(
        username=user.username,
        password=user.password,
        con_id=generate_con_id()
    )
    db.add(user_object)
    db.commit()
    db.refresh(user_object)

    return user_object


async def get_contact(contact_id, db):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        contact = Contact(user_id=contact_id)
        db.add(contact)
        db.commit()
        db.refresh(contact)
    return contact


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
    contact = get_contact(contact_id=contact_user.id, db=db)
    if contact in user.contacts:
        raise HTTPException(
            detail='This user is already contact of this one user',
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    user.contacts.add(contact)
    db.commit()
    db.refresh(user)

    return user
