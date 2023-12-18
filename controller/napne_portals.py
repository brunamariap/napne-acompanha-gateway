from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def indexl():
    return {'message': 'Boa tarde bruno'}

@router.get("/napne/{portal_id}")
def access_portal(portal_id: int):
    return {'message': 'NAPNE system'}