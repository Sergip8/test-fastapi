from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session
from config import settings


oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY =settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRES_MINUTES = settings.access_token_expires_min

def create_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return token

def verify_access_token(token: str, credencials_exeption):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM,])
        user_id = payload.get("user_id") 
        email = payload.get("email")
        if not (user_id and email):
            raise credencials_exeption
        token_data = schemas.TokenData(user_id= user_id, email= email)
        return token_data

    except JWTError as e:
        
        raise credencials_exeption
       
    
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credencials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="no se pudo autenticar el usuario", headers={"WWW-Authenticate": "Bearer"})
    token_claims = verify_access_token(token, credencials_exeption)
    return int(token_claims.user_id)
    