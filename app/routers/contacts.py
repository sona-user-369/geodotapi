import uuid

from fastapi import status, APIRouter, Depends
from app.schemas import users as userschema
from sqlalchemy.orm import Session
from app import db
from app.services import contacts
from app.auth.auth import get_current_user
from typing import Annotated

router = APIRouter(tags=["contacts"], prefix="/contacts")


@router.post('/add/{user_id}/{con_id}', status_code=status.HTTP_200_OK, response_model=userschema.UserScheme)
async def add(user_id: Annotated[uuid.UUID, Depends(get_current_user)], con_id: str,  db: Session = Depends(db.get_db)):
    user = await contacts.add_contact(con_id, user_id, db)
    return user


@router.post('confirm/{user_id}/{contact_id}', status_code=status.HTTP_200_OK)
async def confirm(user_id: Annotated[uuid.UUID, Depends(get_current_user)], contact_id: uuid.UUID, db: Session = Depends(db.get_db)):
    await contacts.confirm_match(user_id, contact_id, db)
