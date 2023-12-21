from fastapi import FastAPI, Depends, Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from gateway.api_router import call_api_gateway, RedirectStudentPortalException, RedirectAcademicManagementPortalException
from controller import napne_portals, authentication
from loguru import logger
from uuid import uuid4
from prisma import Prisma
from security.secure import get_token_data
from jose import JWTError

app = FastAPI()
app.include_router(authentication.router)
app.include_router(napne_portals.router, dependencies=[Depends(call_api_gateway)])

logger.add("info.log", format="Log: [{extra[log_id]}: {time} - {level} - {message}]", level="INFO", enqueue=True)

prisma = Prisma(auto_register=True)

@app.on_event("startup")
def startup():
    prisma.connect()

@app.on_event("shutdown")
def shutdown():
    prisma.disconnect()

# @app.middleware("http")
# async def log_middleware(request: Request, call_next):
#     log_id = str(uuid4())
#     with logger.contextualize(log_id=log_id):
#         logger.info('Request to access ' + request.url.path)
#         try:
#             user = get_token_data(request)
#             response = await call_next(request)
#         except JWTError as jwtException:
#             logger.error(f"Request to " + request.url.path + f" failed: {jwtException}")
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         except Exception as exeception:
#             logger.error(f"Request to " + request.url.path + f" failed: {exeception}")
#             response = JSONResponse(content={"success": False}, status_code=500)
#         finally:
#             logger.info('Successfully accessed ' + request.url.path)
#             return response


@app.exception_handler(RedirectStudentPortalException)
def exception_handler_student(request: Request, exc: RedirectStudentPortalException) -> Response:
    print('entrei aqui')
    return RedirectResponse(url='http://localhost:8003/docs')


@app.exception_handler(RedirectAcademicManagementPortalException)
def exception_handler_academic_management(request: Request, exc: RedirectAcademicManagementPortalException) -> Response:
    return RedirectResponse(url='http://localhost:8001/docs')