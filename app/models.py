from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) 
    role = Column(String, default="user") 
    
    saved_passwords = relationship("PasswordItem", back_populates="owner")

class PasswordItem(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    password_text = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="saved_passwords")