from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users as users_router
from app.routers import contacts as contacts_router

app = FastAPI()
app.include_router(users_router.router)
app.include_router(contacts_router.router)


sio = SocketManager(app=app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

