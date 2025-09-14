# app/router/auth.py

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.depends import CurrentUser
from app.model import User, UserWord
from app.utils.flash import flash, get_flashed_messages

auth_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@auth_router.get('/register', response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request,
                                                        "messages": get_flashed_messages(request)})


@auth_router.post('/register')
def register(request: Request, user: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    password_hash = get_password_hash(password)
    new_user = User(user=user, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    flash(request, "Регистрация успешна! Теперь войдите в систему.", "success")
    return RedirectResponse(url='/login', status_code=303)


@auth_router.get('/login', response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request,
                                                     "messages": get_flashed_messages(request)})


@auth_router.post('/login')
def login(request: Request, user: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    stmt = select(User).where(User.user == user)
    get_user = db.execute(stmt).scalar_one_or_none()
    if not get_user or not verify_password(password, get_user.password_hash):
        flash(request, "Неверное имя пользователя или пароль", "error")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неверное имя пользователя или пароль"})
    request.session["user_id"] = get_user.id
    flash(request, "Добро пожаловать!", "success")
    return RedirectResponse(url="/dashboard", status_code=303)


@auth_router.get('/dashboard', response_class=HTMLResponse)
def dashboard(request: Request, user_id: CurrentUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    words = db.query(UserWord).filter_by(user_id=user_id).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "words": words,
                                                         "messages": get_flashed_messages(request)})


@auth_router.get('/logout', response_class=HTMLResponse)
def logout(request: Request):
    flash(request, "Вы вышли из системы!", "success")
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
