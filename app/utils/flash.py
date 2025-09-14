#/home/zidan/PycharmProjects/EnglishTrainer/app/utils/flash.py
from fastapi import Request


def flash(request: Request, message: str, category: str = 'info'):
    if 'flash' not in request.session:
        request.session['flash'] = []
    request.session["flash"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    messages = request.session.pop('flash', [])
    return messages
