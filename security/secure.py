from fastapi import Depends, HTTPException, status, Request
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from repository.user import UserRepository
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_PASSPHRASE")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="ch07/login/token")

def get_password_hash(password):
    return crypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)

def authenticate(password, passphrase):
    try:
        password_check = verify_password(password, passphrase)
        return password_check
    except Exception as e:
        print(e)
        return False
    
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({ "exp": expire })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def get_token_data(request: Request):
    token = request.headers.get('authorization').split(" ")[1]
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(decoded_token)
        return decoded_token
    except JWTError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    user_repository = UserRepository()
    user = user_repository.get_by_registration(token)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user