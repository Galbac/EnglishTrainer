# app/depends.py
from typing import Annotated

from fastapi import Request, Depends
from fastapi.exceptions import HTTPException


def get_current_user_id(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=303,
            detail="Пользователь не авторизован, перенаправление на страницу входа",
            headers={"Location": "/login"},
        )
    return user_id

CurrentUser = Annotated[int, Depends(get_current_user_id)]
