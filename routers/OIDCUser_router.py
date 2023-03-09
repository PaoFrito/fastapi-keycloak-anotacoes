""" OIDCUser representa um usuário autenticado e autorizado pelo servidor Keycloak """
""" Contém informações sobre o usuário, nome de usuário, ID, e-mail e as funções ou grupos aos quais o usuário pertence. """

from fastapi import APIRouter, HTTPException, Depends
from fastapi_keycloak import OIDCUser, has_group
from anotacoes import main

router = APIRouter(prefix="/users")

# Rota não protegida com autenticação do Keycloak   
@router.get("/unprotected")
async def protected_route():
    return {"message": "Olá Anonimo! Você tem permissão para acessar esta rota."}

# Rota protegida com autenticação do Keycloak   
@router.get("/protected")
@main.idp.keycloak_protect() # Middleware de autenticação
async def protected_route(user: OIDCUser):
    return {"message": f"Olá, {user.username}! Você tem permissão para acessar esta rota."}

# Rota nao protegida, mas exige autenticacao igual
@router.get("/user")  
async def current_users(user: OIDCUser = Depends(main.idp.get_current_user())): # Autenticação feita através de validação (igual validação do pydantic), não usa middleware
    return user

# Rota protegida com autenticação do Keycloak
@router.get("/adm")
@main.idp.keycloak_protect() # Middleware de autenticação
async def adm_protected_route(user: OIDCUser):
    if not has_group(user, "admin"): # Validação de grupo. 'has_group' é uma função do fastapi_keycloak
        raise HTTPException(status_code=403, detail="Acesso negado: você precisa ser um administrador para acessar esta rota.")
    return {"message": "Bem-vindo, administrador!"}

# Rota nao protegida com validacao. Sem middleware
@router.get("/rcl")
async def protected(user: OIDCUser = Depends(main.idp.get_current_user(required_roles=["reciclometro"]))): #Uso do objeto idp para autenticar e validar a role do usuário
    return "Olá usuario com a role reciclometro"