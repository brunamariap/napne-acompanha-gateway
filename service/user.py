from repository.user import UserRepository
from prisma.partials import UserRequest
from prisma.enums import Departments
from security import secure
from security.suap_api import Suap
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from security import secure


class UserService:

    def __init__(self):
        self.repository = UserRepository()
    
    def authenticateUser(self, request: UserRequest):
        user_exists = self.repository.get_by_registration(request.registration)
        
        if (user_exists):
            password_match = secure.authenticate(request.password, user_exists.password)
            
            if password_match:
                token = secure.create_access_token(user_exists.dict())

                return {"user": user_exists, "access_token": token, "token_type": "bearer"}
            
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail={"detail": "Senha incorreta"})

        else:
            suap_repository = Suap()
            response = suap_repository.authenticate(request.registration, request.password)
            if response['success']:
                department = Departments.ADMINISTRATOR if response['department'] == 'Servidor' else Departments.TEACHER

                if not department:
                    raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail={'detail': 'Usuário não autorizado'})

                hashed_password = secure.get_password_hash(request.password)
                new_user = {
                    "name": response['name'], 
                    "registration": request.registration, 
                    "password": hashed_password, 
                    "department": department, 
                    "picture": response['picture']
                }

                created_user = self.repository.create(new_user)
                token = secure.create_access_token(created_user.dict())

                return {"user": created_user, "access_token": token, "token_type": "bearer"}
            
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(response))
        

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: str):
        return self.repository.get_by_id(id)

    def change(self, id: str, request: UserRequest):
        return self.repository.change(id, request)

    def remove(self, id: str):
        return self.repository.remove(id)
