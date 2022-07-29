from typing import Optional, List
from fastapi import Depends, Body, FastAPI, Response, status, HTTPException, APIRouter
from .. import models, schemas, oauth
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

# Note authentication was added to all routes, but it depends on what you need.
# Router to connect with main.py. Prefix is used to simplify routers in this file.
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Get all posts
# ?limit=3 limits to 3 posts.
# & to add another query parameter
# skip will skip over
# search will search for text for a match
#
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #Serialize and pass as json
    return results

# Create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000000)
    # my_posts.append(post_dict)

    # Did not do as f string to avoid sql injections
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    

    # Convert to a dict to efficiently create new_post.
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()

    # Refresh and retrieve and store it back into new_post
    db.refresh(new_post) 

    return new_post

# Get a specific post
# Use path parameter id to determine which post to look at
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id : int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post

# Delete posts
# 204 does not return any data   
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    #delete post
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update posts
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_info = post_query.first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    
    if post_info.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    #Understand why **post.dict does not work here
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
