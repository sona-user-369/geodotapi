from app import settings
from app.models import users as usermodel
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose.jwt import encode, decode
from app.models.users import Token
from typing import Annotated
from app import db as database
from app.utils import helpers

oauth_scheme = OAuth2PasswordBearer(tokenUrl='users/login')


def get_current_user(token: Annotated[str, Depends(oauth_scheme)], db: Session = Depends(database.get_db)):
    username = None
    try:
        decoded_data = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = decoded_data.get("sub")
        if not sub:
            raise HTTPException(
                detail='Token is invalid',
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
        username = sub
        db_token = db.query(Token).filter(Token.key == token).first()
        if not db_token:
            raise HTTPException(
                detail='Token is invalid',
                status_code=status.HTTP_406_NOT_ACCEPTABLE
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    user = db.query(usermodel.User).filter(usermodel.User.username == username).first()
    return user


async def authenticate_user(data, db: Session):
    authenticate_exception = HTTPException(
        detail="unable to authenticate this user",
        status_code=status.HTTP_401_UNAUTHORIZED
    )
    user = db.query(usermodel.User).filter(usermodel.User.username == data.username).first()
    if not user or not helpers.check_pass(user.password, data.password):
        raise authenticate_exception


async def create_access_token(data: dict, user_id: str, db: Session):
    data_copy = data.copy()
    encoded_data = encode(data_copy, settings.SECRET_KEY, algorithm=[settings.ALGORITHM])
    object_token = Token(
        user_id=user_id,
        key=encoded_data
    )

    db.add(object_token)
    db.commit()
    db.refresh(object_token)
    return encoded_data
