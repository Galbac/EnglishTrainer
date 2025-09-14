#app/router/words.py
import random
from http.client import HTTPResponse

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.depends import CurrentUser
from app.model import Word, UserWord

words_router = APIRouter()
templates = Jinja2Templates("app/templates")
print("templates", templates.get_template("add_word.html"))


@words_router.get("/add_word")
def add_word_page(request: Request):
    return templates.TemplateResponse("add_word.html", {"request": request})


@words_router.post("/add_word")
def add_word(request: Request, user_id: CurrentUser, english: str = Form(...), russian: str = Form(...),
             db: Session = Depends(get_db)):
    # Проверим, есть ли слово в базе
    word = db.query(Word).filter(Word.english == english).first()
    if not word:
        word = Word(english=english, russian=russian)
        db.add(word)
        db.commit()
        db.refresh(word)

    # Связываем слово с пользователем (если ещё не добавлено)
    user_word = db.query(UserWord).filter_by(user_id=user_id, word_id=word.id).first()
    if not user_word:
        user_word = UserWord(user_id=user_id, word_id=word.id, progress=0)
        db.add(user_word)
        db.commit()

    return RedirectResponse('/dashboard', status_code=303)


@words_router.get('/test', response_class=HTTPResponse)
def test_page(request: Request, user_id: CurrentUser, db: Session = Depends(get_db)):
    user_words = db.query(UserWord).filter_by(user_id=user_id).all()
    if not user_words:
        return templates.TemplateResponse('test.html', {'request': request, 'word': None})

    chosen = random.choice(user_words)
    mode = random.choice(["en->ru", "ru->en"])
    return templates.TemplateResponse('test.html', {'request': request, 'word': chosen, 'mode': mode})


@words_router.post('/test')
def check_answer(request: Request, user_id: CurrentUser, mode: str = Form(...),
                 answer: str = Form(...), userword_id: int = Form(...), db: Session = Depends(get_db)):
    user_word = db.query(UserWord).filter_by(id=userword_id, user_id=user_id).first()
    if not user_word:
        return RedirectResponse('/test', status_code=303)

    correct = None
    if mode == "en->ru":
        correct = user_word.word.russian.lower()
    elif mode == "ru->en":
        correct = user_word.word.english.lower()
    if answer.strip().lower() == correct:
        user_word.progress = min(100, user_word.progress + 10)
        db.commit()
        result = "Верно"
    else:
        user_word.progress = max(0, user_word.progress - 5)
        db.commit()
        result = f"❌ Неверно! Правильный ответ: {correct}"
    return templates.TemplateResponse("test_result.html", {"request": request, "result": result})
