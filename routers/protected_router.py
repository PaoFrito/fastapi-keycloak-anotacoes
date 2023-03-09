from fastapi import APIRouter
from main import idp

router = APIRouter()

# Rota protegida com autenticação do Keycloak
@router.get("/protected")
@idp.keycloak_protect()
async def protected_route():
    return {"message": "Esta rota é protegida pelo Keycloak!"}