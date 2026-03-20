from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import password, auth 
from app.database import init_db
from app import models

init_db()

app = FastAPI(title="Password Lab")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth.router)
app.include_router(password.router)