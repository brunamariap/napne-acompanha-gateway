from fastapi import APIRouter

# Essas duas linhas abaixo precisam ser colocadas no router das rotas que precisam ser protegidas

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentication/token", description="Autenticação JWT")
#router = APIRouter(dependencies=[Depends(oauth2_scheme), Depends(get_token_data)])

router = APIRouter()

@router.get("/")
def indexl():
    return {'message': f'Bem vindo ao portal NAPNE Acompanha!'}

@router.get("/napne/{portal_id}/{path:path}")
def access_portal(portal_id: str):
    return {'message': 'NAPNE system'}