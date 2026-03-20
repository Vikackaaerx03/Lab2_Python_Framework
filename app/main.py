from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import password

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(password.router)