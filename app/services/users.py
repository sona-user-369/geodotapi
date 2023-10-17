import random
import string
from sqlalchemy.orm import Session
from app.models.users import User


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


async def add_contact(contact_id, user_id, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
