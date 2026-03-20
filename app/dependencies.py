from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

def get_current_user(request: Request, db: Session = Depends(get_db)):
    username = request.cookies.get("username")
    
    if username:
        user = db.query(models.User).filter(models.User.username == username).first()
        return user
        
    return None