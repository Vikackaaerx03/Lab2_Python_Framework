from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import re

from app.database import get_db
from app import models
from app.dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# --- СТОРІНКА ВХОДУ ---
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if not user or user.password != password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Невірний логін або пароль!"})
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="username", value=username)
    return response

# --- СТОРІНКА РЕЄСТРАЦІЇ ---
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
         return templates.TemplateResponse("register.html", {"request": request, "error": "Цей логін вже зайнятий!"})
    
    if len(password) < 14:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Мінімум 14 символів."})
    elif not re.search(r"[A-Z]", password):
        return templates.TemplateResponse("register.html", {"request": request, "error": "Додайте велику літеру (A-Z)."})
    elif not re.search(r"[a-z]", password):
        return templates.TemplateResponse("register.html", {"request": request, "error": "Додайте малу літеру (a-z)."})
    elif not re.search(r"[_\-!@#$%^&*(),.?\":{}|<>]", password):
        return templates.TemplateResponse("register.html", {"request": request, "error": "Додайте спецсимвол (@, $, % тощо)."})

    new_user = models.User(username=username, password=password, role="user")
    db.add(new_user)
    db.commit()
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="username", value=username)
    return response

# --- АДМІН-ПАНЕЛЬ ---
@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(
    request: Request, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    all_users = db.query(models.User).all()
    all_passwords = db.query(models.PasswordItem).all()
    
    return templates.TemplateResponse("admin.html", {
        "request": request, 
        "user": user, 
        "users_list": all_users,
        "passwords_list": all_passwords
    })

# Функція видалення користувача
@router.get("/admin/delete/user/{user_id}")
async def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    if user_to_delete and user_to_delete.username != user.username:
        db.delete(user_to_delete)
        db.commit()
        
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

# Функція видалення ПАРОЛЯ
@router.get("/admin/delete/password/{password_id}")
async def delete_password(
    password_id: int, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    pass_to_delete = db.query(models.PasswordItem).filter(models.PasswordItem.id == password_id).first()
    if pass_to_delete:
        db.delete(pass_to_delete)
        db.commit()
        
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

# --- ВИХІД ---
@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="username")
    return response