import logging
from fastapi import Request


logger = logging.getLogger('uvicorn.access')

def call_api_gateway(request: Request):
    portal_id = request.path_params['portal_id']

    if portal_id == str(1):
        raise RedirectStudentPortalException()
    elif portal_id == str(2):
        raise RedirectAcademicManagementPortalException()
    

class RedirectStudentPortalException(Exception):
    pass

class RedirectAcademicManagementPortalException(Exception):
    pass