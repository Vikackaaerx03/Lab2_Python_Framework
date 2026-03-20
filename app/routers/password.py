from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import re
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/check", response_class=HTMLResponse)
async def check_password(request: Request, password: str = Form(...)):
    # 1. Перевірка довжини
    length_ok = len(password) >= 12
    
    # 2. Наявність цифри
    has_digit = any(char.isdigit() for char in password)
    
    # 3. Наявність великої літери
    has_upper = any(char.isupper() for char in password)
    
    # 4. Наявність малої літери
    has_lower = any(char.islower() for char in password)
    
    # 5. Наявність спеціального символу
    has_special = bool(re.search(r"[_\-!@#$%^&*(),.?\":{}|<>]", password))

    # Пароль надійний, якщо всі умови True
    is_secure = all([length_ok, has_digit, has_upper, has_lower, has_special])
    
    tips = []
    if not length_ok: tips.append("Довжина має бути не менше 12 символів")
    if not has_upper: tips.append("Додайте хоча б одну велику літеру (A-Z)")
    if not has_lower: tips.append("Додайте хоча б одну малу літеру (a-z)")
    if not has_digit: tips.append("Додайте хоча б одну цифру (0-9)")
    if not has_special: tips.append("Додайте спецсимвол (наприклад: @, _, $, %)")

    context = {
        "request": request,
        "password": password,
        "password_length": len(password),
        "is_secure": is_secure,
        "tips": tips
    }
    
    return templates.TemplateResponse("result.html", context)