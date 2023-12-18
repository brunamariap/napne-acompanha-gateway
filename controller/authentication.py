from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
from repository.user import UserRepository
from prisma.partials import UserRequest, UserResponse, UserAuthentication
from security import secure
router = APIRouter(prefix="/authentication", tags=["Autenticação"])

user_service = UserRepository

@router.post("/login")
def login(request: UserAuthentication) -> UserResponse:
    user_exists = user_service.get_by_registration(request.registration)

    if (user_exists):
        password_match = secure.authenticate(request.password, user_exists.passphrase)
        
        if password_match:
            return JSONResponse(content=jsonable_encoder(user_exists), status_code=status.HTTP_200_OK)
        
        return JSONResponse(content={"details": "Senha incorreta"}, status_code=status.HTTP_400_BAD_REQUEST)

    else:
        return JSONResponse(content=jsonable_encoder(user_exists), status_code=status.HTTP_404_NOT_FOUND)