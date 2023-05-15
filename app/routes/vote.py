from typing import Optional, List

from fastapi import Depends,APIRouter , HTTPException, status
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, utils, oauth2

router = APIRouter(prefix="/vote", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_vote(vote: schemas.Vote, db: Session = Depends(get_db)
                   , current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                             detail=  f"post con el id {vote.post_id} no existe") 

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user)
    _vote = vote_query.first()
    
    if _vote:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return "voto removido"
    else:
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user)
        db.add(new_vote)
        db.commit()
        return "voto añadido"
        