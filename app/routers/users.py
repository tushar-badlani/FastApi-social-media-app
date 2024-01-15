from .. import models, schemas, utils, oauth
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = utils.get_password_hash(user.password)
    user.password = hashed
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user

@router.post("/reset", status_code=status.HTTP_202_ACCEPTED)
async def reset_password(user: schemas.UserResetPassword, db: Session = Depends(get_db)):
    TEMP_TOKEN_EXPIRE_MINUTES = 10
    user = db.query(models.User).filter(models.User.email == user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        token = oauth.create_reset_token(user.email, expires_delta=TEMP_TOKEN_EXPIRE_MINUTES)
        await utils.send_reset_password_email(user.email, token)
        return {"message": "Password reset email sent"}
