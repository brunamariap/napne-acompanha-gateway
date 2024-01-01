from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from gateway.api_router import call_api_gateway, RedirectStudentPortalException, RedirectAcademicManagementPortalException
from controller import napne_portals, authentication
from loguru import logger
from prisma import Prisma
import os

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://napne.azurewebsites.net",
    os.getenv("MS_STUDENT_URL"),
    os.getenv("MS_ACADEMIC_MANAGEMENT_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return RedirectResponse(url=os.getenv("MS_STUDENT_URL") +request.url.path)


@app.exception_handler(RedirectAcademicManagementPortalException)
def exception_handler_academic_management(request: Request, exc: RedirectAcademicManagementPortalException) -> Response:
    return RedirectResponse(url=os.getenv("MS_ACADEMIC_MANAGEMENT_URL")+request.url.path)