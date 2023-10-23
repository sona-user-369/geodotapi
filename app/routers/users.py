from fastapi import APIRouter, status, Response, Depends
from app.schemas import users as userschema
from app.services import users as userservice
from typing import Annotated
from app import db
from sqlalchemy.orm import Session
from app.auth import auth


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/register", status_code=status.HTTP_200_OK, response_model=userschema.UserScheme)
async def register(request: Annotated[userschema.UserSchemeCreate, Depends()], db: Session = Depends(db.get_db)):
    user = await userservice.register_user(request, db)
    return user


@router.post("/login", status_code=status.HTTP_200_OK, response_model=userschema.TokenScheme)
async def login(request: Annotated[userschema.Auth, Depends()], db: Session = Depends(db.get_db)):
    token = None
    user = await auth.authenticate_user(request, db)
    if user:
        token = await auth.create_access_token({"sub": user.username}, user.id, db)
        print(token)

    return {
        "token": token,
        "type": "Bearer",
        "user": user
    }


@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(token=Depends(auth.get_token), db: Session = Depends(db.get_db)):
    await userservice.logout_user(token, db)


