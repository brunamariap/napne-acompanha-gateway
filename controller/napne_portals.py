from fastapi import APIRouter, Request, Header
from fastapi import Depends
from security.secure import get_current_user, get_token_data
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from security import secure

# Essas duas linhas abaixo precisam ser colocadas no router das rotas que precisam ser protegidas
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentication/token", description="Autenticação JWT")
#router = APIRouter(dependencies=[Depends(oauth2_scheme), Depends(get_token_data)])
router = APIRouter()

@router.get("/")
def indexl():
    return {'message': f'Bem vindo ao portal NAPNE Acompanha!'}

@router.get("/napne/{portal_id}")
def access_portal(portal_id: int):
    return {'message': 'NAPNE system'}