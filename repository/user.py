from prisma.models import User
from prisma.partials import UserRequest
from typing import Optional

class UserRepository:

    def __init__(self):
        self.repository = User

    def create(self, request: UserRequest):
        return self.repository.prisma().create(request)

    def get_by_id(self, id):
        return self.repository.prisma().find_unique({'id': id})
    
    def get_by_registration(self, registration) -> User:
        return self.repository.prisma().find_first(where={
            "registration": registration
        })

    def change(self, id: str, request: UserRequest):
        return self.repository.prisma().update(data=request, where={'id': id})