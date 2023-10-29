import uuid

from fastapi import status, APIRouter, Depends
from app.schemas import users as userschema
from sqlalchemy.orm import Session
from app import db
from app.services import contacts
from app.auth.auth import get_current_user
from typing import Annotated, List
from ..utils.helpers import cache



router = APIRouter(tags=["contacts"], prefix="/contacts")


@router.post('/add/{con_id}', status_code=status.HTTP_200_OK, response_model=userschema.UserScheme)
async def add(current_user: Annotated[userschema.UserScheme, Depends(get_current_user)], con_id: str,  db: Session = Depends(db.get_db)):
    user = await contacts.add_contact(con_id, current_user.id, db)
    return user


@router.post('/confirm/{contact_id}', status_code=status.HTTP_200_OK)
async def confirm(current_user: Annotated[userschema.UserScheme, Depends(get_current_user)], contact_id: uuid.UUID, db: Session = Depends(db.get_db)):
    await contacts.confirm_match(current_user.id, contact_id, db)


@router.get('/get', status_code=status.HTTP_200_OK, response_model=List[userschema.ContactScheme])
async def get_contacts(current_user: Annotated[userschema.UserScheme, Depends(get_current_user)], db: Session = Depends(db.get_db)):
    return await contacts.get_contacts(current_user.id, db)


@router.get('/get/totals', status_code=status.HTTP_200_OK)
async def get_totals(current_user: Annotated[userschema.UserScheme, Depends(get_current_user)], db: Session = Depends(db.get_db)):
    db_contacts = await contacts.get_contacts(current_user.id, db)
    total_contacts = len(db_contacts)
    total_connected = 0
    
    for contact in db_contacts:
        if cache.get(contact.id):
            total_connected = + 1

    return {"total_contacts": total_contacts, "total_connected": total_connected}