from .. import models, schemas, oauth
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if vote.dir == 1:
        query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id).filter(models.Votes.user_id == current_user.id)
        vote_found = query.first()
        if(vote_found):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted")
        else:
            new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {"message": "Vote created successfully"}
    else:
        query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id).filter(models.Votes.user_id == current_user.id)
        vote_found = query.first()
        if(vote_found):
            query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not voted yet")