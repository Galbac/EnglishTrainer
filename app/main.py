#app/main.py
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.router.auth import auth_router
from app.router.words import words_router

load_dotenv()
SECRET_KEY_MIDDLEWARE = os.getenv("SECRET_KEY_MIDDLEWARE")
app = FastAPI()

app.include_router(auth_router)

app.include_router(words_router)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY_MIDDLEWARE)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
