from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware
from pydantic.v1 import ValidationError
from fastapi.responses import JSONResponse

from app.routers import users as users_router
from app.routers import contacts as contacts_router

app = FastAPI(title="GeoDot")
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


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    # print(exc.json())
    print(exc.errors)
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(content={"errors": errors}, status_code=400)
#

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)