import uuid

from fastapi import status, APIRouter
from app.schemas import users as userschema
from sqlalchemy.orm import Session
from app import  db

router = APIRouter(tags=["contacts"], prefix="/contacts")


@router.post('/add/{user_id}', status_code=status.HTTP_200_OK, response_model=userschema.UserScheme)
async def add(user_id: uuid.UUID, db: Session = db.get_db()):
    pass
