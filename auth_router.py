from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.connection import get_db
from database.orm import User
from database.repository import create_user, get_user_by_email
from oauth import oauth  # main.py 혹은 app의 설정을 import 해야 합니다.
import requests

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



@router.post("/get-me/")
async def get_user_info(token_data: TokenData):
    google_userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {token_data.token}"}
    response = requests.get(google_userinfo_url, headers=headers)
    
    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        raise HTTPException(status_code=response.status_code, detail="사용자 정보를 조회할 수 없습니다.")