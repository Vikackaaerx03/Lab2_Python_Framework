from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import re
import os
from app.dependencies import get_current_user
from app.database import get_db
from app import models

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Головна сторінка
@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request, user: models.User = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

# Сторінка перевірки
@router.post("/check", response_class=HTMLResponse)
async def check_password(
    request: Request, 
    password: str = Form(...),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Захист! Якщо користувач не увійшов, повертаємо його назад
    if not user:
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "user": None,
                "error": "Щоб перевірити пароль, потрібно увійти або зареєструватися!"
            }
        )

    # --- ЛОГІКА ПЕРЕВІРКИ ПАРОЛЯ ---
    length_ok = len(password) >= 12
    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_special = bool(re.search(r"[_\-!@#$%^&*(),.?\":{}|<>]", password))

    is_secure = all([length_ok, has_digit, has_upper, has_lower, has_special])
    
    tips = []
    if not length_ok: tips.append("Довжина має бути не менше 12 символів")
    if not has_upper: tips.append("Додайте хоча б одну велику літеру (A-Z)")
    if not has_lower: tips.append("Додайте хоча б одну малу літеру (a-z)")
    if not has_digit: tips.append("Додайте хоча б одну цифру (0-9)")
    if not has_special: tips.append("Додайте спецсимвол (наприклад: @, _, $, %)")

    # НОВЕ: Зберігаємо пароль ТІЛЬКИ якщо він надійний
    if is_secure:
        new_password_record = models.PasswordItem(
            password_text=password,
            user_id=user.id # Прив'язуємо пароль до поточного користувача
        )
        db.add(new_password_record)
        db.commit()

    context = {
        "request": request,
        "password": password,
        "password_length": len(password),
        "is_secure": is_secure,
        "tips": tips,
        "user": user 
    }
    
    return templates.TemplateResponse("result.html", context)