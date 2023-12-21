from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
from repository.user import UserRepository
from prisma.models import User
from prisma.partials import UserRequest, UserAuthRequest
from security.suap_api import Suap
from security import secure
from service.user import UserService
from pydantic import BaseModel

router = APIRouter(prefix="/authentication", tags=["Autenticação"])
user_service = UserService()

class UserResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

@router.post("/login")
def login(request: UserAuthRequest) -> UserResponse:
    return JSONResponse(content=jsonable_encoder(user_service.authenticateUser(request)), status_code=status.HTTP_200_OK)