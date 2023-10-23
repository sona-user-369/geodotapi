import random
import string
from sqlalchemy.orm import Session
from app.models.users import User, Token
from app.models.contacts import Contact
from fastapi import HTTPException, status
from app.utils import  helpers


async def generate_con_id():
    generated_key = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    generated_id = 'con{0}up'.format(generated_key)
    print(generated_id)
    return generated_id


async def register_user(user, db: Session):
    user_object = User(
        username=user.username,
        password=helpers.crypt_pass(user.password),
        con_id=await generate_con_id()
    )
    db.add(user_object)
    db.commit()
    db.refresh(user_object)

    return user_object


async def logout_user(token, db: Session):
    token_object = db.query(Token).filter(Token.key == token).delete()
    db.commit()
    db.refresh(token_object)

