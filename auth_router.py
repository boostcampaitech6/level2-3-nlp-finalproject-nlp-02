import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import User
from database.repository import create_user, get_user_by_email
from oauth import oauth  # main.py 혹은 app의 설정을 import 해야 합니다.

router = APIRouter()


class TokenData(BaseModel):
    token: str


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route("/auth")
async def auth(request: Request, session: Session = next(get_db())):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token["userinfo"]

    tempuser: User = User.create(request=userinfo)
    user: User | None = get_user_by_email(session=session, email=tempuser.email)

    if not user:
        create_user(session=session, user=tempuser)

    request.session["user_info"] = userinfo

    return RedirectResponse(url="/session", status_code=303)


@router.get("/me")
async def get_current_user(request: Request, session: Session = Depends(get_db)):
    user_info = request.session.get("user_info")

    if user_info:
        return get_user_by_email(session=session, email=user_info["email"])

    return {"message": "no session"}


def get_current(token: TokenData) -> User:
    google_userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(google_userinfo_url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()

        return user_info


@router.get("/get-me")
async def get_user_info(request: Request, session: Session = Depends(get_db)):
    user_info = get_current(token=request.headers.get("Access-Token"))
    user_email = user_info.get("email")

    user: User = get_user_by_email(session=session, email=user_email)

    return {"name": user.name, "streak": user.streak}
