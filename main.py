import os
from fastapi import FastAPI
from fastapi_keycloak import FastAPIKeycloak
from anotacoes.routers import protected_router
from anotacoes.routers import all_routers_protected
from anotacoes.routers import OIDCUser_router

app = FastAPI(
    title="API de Autenticação e Autorização com Keycloak",
    version=os.getenv("PROJECT_VERSION", "Unknown version"),
)

keycloak_url = os.environ['KEYCLOAK_AUTH_URL']
realm_name = os.environ['KEYCLOAK_REALM']

# Objeto que conecta o serviço ao Keycloak. Também é usado para proteger os endpoints
idp = FastAPIKeycloak(
    #Url do Keycloak
    server_url = keycloak_url,
    
    #ID do cliente
    client_id = os.environ['KEYCLOAK_CLIENT_ID'],
    
    #Secrete do cliente 
    client_secret = os.environ['KEYCLOAK_CLIENT_SECRET'],
    
    #Secret do adm_cli
    admin_client_secret = os.environ['KEYCLOAK_ADM_CLIENT_SECRET'],
    
    #Reaml que o cliente esta
    realm = realm_name,
    
    #Endpoint que fornece as chaves públicas usadas para verificar a assinatura do token de autenticação do Keycloak
    public_key_url = f"{keycloak_url}/realms/{realm_name}/protocol/openid-connect/certs",
    
    #URL base do Keycloak usada como emissor do token de autenticação
    issuer_url = f"{keycloak_url}/realms/{realm_name}",
    
    #Rota da callback definida no keycloak (ainda nao sei dizer se é necessario em todos os microservicos)
    callback_uri = (os.environ['AAK_URL'] + '/callback'),
)

#Inclui os endpoints dos routers a instancia prin cipal do projeto (app)
app.include_router(protected_router.router)
app.include_router(all_routers_protected.router)
app.include_router(OIDCUser_router.router)

#Adiciona middleware de autenticacao a todos os endpoints do router 
idp(all_routers_protected.router)