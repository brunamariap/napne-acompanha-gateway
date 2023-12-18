from fastapi import APIRouter


router = APIRouter()

@router.get("/napne/{portal_id}")
def acsess_portal(portal_id: int):
    return {'message': 'NAPNE system'}