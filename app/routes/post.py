from typing import Optional, List

from fastapi import Depends,APIRouter , HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, utils, oauth2

router = APIRouter(prefix="/post", 
                   responses={404: {"message": "No hay de eso"}},
                   tags=["post"])



@router.post("/create_post", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(owner_id= user_id, **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[schemas.PostOut])
def get_all_post(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] =""):
    #post_query = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip)

    return post_query.all()

@router.get("/user", response_model=List[schemas.PostResponse])
def get_all_user_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.owner_id == user_id).all()
    return post

@router.get("/{id}", response_model=schemas.PostOut)
async def get_post_by_id(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts where posts.id = %s""", (str(id),))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                             detail=  f"post con el id {id} no existe") 
        
    return post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""DELETE FROM posts where posts.id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    if not post.first():
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                             detail=  f"post con el id {id} no existe") 
    #conn.commit()
    
    if post.first().owner_id != user_id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                             detail=  "este no es su post puto") 
    post.delete(synchronize_session=False)
    db.commit()
    
    
@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    if not post_query.first():
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                             detail=  f"post con el id {id} no existe") 
    #conn.commit()
  
    if post_query.first().owner_id != user_id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                             detail=  "este no es su post puto") 

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()