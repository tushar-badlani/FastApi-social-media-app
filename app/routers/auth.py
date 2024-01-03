from fastapi import APIRouter, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth, schemas


router = APIRouter(
    # prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user_query:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    else:
        if not utils.verify_password(user_cred.password, user_query.password):
            raise HTTPException(status_code=404, detail="Invalid credentials")
        else:
            access_token = oauth.create_access_token(data={"user_id": user_query.id})
            return {"access_token": access_token, "token_type": "bearer"}
