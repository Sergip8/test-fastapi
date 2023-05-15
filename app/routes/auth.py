
from fastapi import Depends,APIRouter , HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["auth"])

@router.post("/login", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=  f"email o password incorrectos") 
    
    if not utils.verify(user.password, user_credentials.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail=  f"email o password incorrectos") 
    
    token = oauth2.create_token(data= {"user_id": user.id, "email": user.email})

    return {"access_token": token, "token_type": "bearer"}