from .. import models, schemas, oauth
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("SELECT * FROM posts;")
    # posts = cursor.fetchall()
    # print(posts)
    # return {"data": posts}

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    results = db.query(models.Post, func.count(models.Votes.post_id).label('total_votes')).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth.get_current_user)):
    new_post = models.Post(title=post.title, content=post.content, published=post.published, owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Votes.post_id).label('total_votes')).join(models.Votes,
                                                                                                models.Post.id == models.Votes.post_id,
                                                                                                isouter=True).group_by(
        models.Post.id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        if post_query.first().owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this post")
        post_query.delete(synchronize_session=False)
        db.commit()
        return {"data": "Post deleted successfully"}


@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        if post_query.first().owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to update this post")
        post_query.update(post.dict())
        db.commit()
        return {"data": "Post updated successfully"}


@router.post("/{id}/comment", status_code=status.HTTP_201_CREATED)
def create_comment(id: int, comment: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        new_post = models.Post(title=comment.title, content=comment.content, published=comment.published, owner_id=current_user.id, commented_on_id=id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post


@router.get("/{id}/comments", response_model=List[schemas.Comment])
def get_comments(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        comments = db.query(models.Post).filter(models.Post.commented_on_id == id).all()
        return comments
