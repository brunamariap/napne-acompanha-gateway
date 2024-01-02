from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
from prisma.partials import UserResponse
from service.user import UserService

router = APIRouter(prefix="/users", tags=["Usuário"])

userService = UserService()

@router.get("/{user_id}/details")
def get_user_details(user_id: str) -> UserResponse:
    return JSONResponse(content=jsonable_encoder(userService.get_by_id(user_id)), status_code=status.HTTP_200_OK)