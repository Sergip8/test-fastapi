
from fastapi import Depends,APIRouter , HTTPException, status

from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, utils

router = APIRouter(prefix="/user", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["user"])

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponse)    
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                             detail=  f"el email ya esta registrado") 
    
@router.get("/{id}", response_model= schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                             detail=  f"usuario con el id {id} no existe") 

    return user