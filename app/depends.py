# app/depends.py
from typing import Annotated

from fastapi import Request, Depends
from fastapi.responses import RedirectResponse


def get_current_user_id(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)
    return user_id


CurrentUser = Annotated[int, Depends(get_current_user_id)]
