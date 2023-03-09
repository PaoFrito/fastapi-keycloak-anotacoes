#Várias rotas não protegidas. A proteção é feita no main.py

from fastapi import APIRouter

router = APIRouter(prefix="/protegido")

@router.get("/")
async def read_root():
    return {"message": "Hello World"}

@router.get("/items/")
async def read_items():
    return [{"item_name": "dice"}]

@router.get("/users/")
async def read_users():
    return [{"username": "JohnDoe"}]