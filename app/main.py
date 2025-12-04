from typing import Union

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api.endpoints import users, auth, activity, organization, report



origins = [
    "*"
]



app = FastAPI(
    redoc_url="/documentation",
    title="My API",
    description="API documentation with ReDoc",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(activity.router)
app.include_router(organization.router)
app.include_router(report.router)

class Item(BaseModel):
    name : str
    price : float
    is_offer : Union[bool, None] = None

@app.get("/health")
def read_root():
    return {"status": "Ok!"}

