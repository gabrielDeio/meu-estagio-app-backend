from typing import Union

from pydantic import BaseModel
from fastapi import FastAPI

from app.api.endpoints import users
from app.api.endpoints import auth

app = FastAPI()


app.include_router(users.router)
app.include_router(auth.router)

class Item(BaseModel):
    name : str
    price : float
    is_offer : Union[bool, None] = None

@app.get("/health")
def read_root():
    return {"status": "Ok!"}

