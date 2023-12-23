import logging
from fastapi import Request


logger = logging.getLogger('uvicorn.access')

def call_api_gateway(request: Request):
    
    portal_id = request.path_params['portal_id']
    request.scope["path"] = request.url.path.replace(f"/napne/{portal_id}", "")
    
    if portal_id == "student":
        raise RedirectStudentPortalException()
    elif portal_id == "academic":
        raise RedirectAcademicManagementPortalException()
    

class RedirectStudentPortalException(Exception):
    pass

class RedirectAcademicManagementPortalException(Exception):
    pass