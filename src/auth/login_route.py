from fastapi import APIRouter
from ..models.entities.login_entity import Login

login_router = APIRouter(
    prefix="/login",
    tags=["login"]
)

@login_router.post("/")
async def login(login: Login):
    return {"message": "Login successful", "login": login}