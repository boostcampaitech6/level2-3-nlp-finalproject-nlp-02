import requests
from database.connection import get_db
from database.orm import User
from database.repository import create_update_user, get_user_by_email
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from oauth import oauth  # main.py 혹은 app의 설정을 import 해야 합니다.
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter()


class TokenData(BaseModel):
    token: str


@router.get("/login")
async def login(request: Request):
    # 구글 로그인 페이지로 리다이렉트
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route("/auth")
async def auth(request: Request, session: Session = next(get_db())):
    # OAuth 로그인 콜백. 사용자를 체크하는 get_or_create_user 함수 실행
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    userinfo = token.get("userinfo")
    if not userinfo:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token has no information")

    user_email = userinfo.get("email")
    if not user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token has no information")

    find_create_user(session, userinfo)
    request.session["user_info"] = userinfo  # 사용자 정보를 세션에 저장

    return RedirectResponse(url="/session", status_code=status.HTTP_303_SEE_OTHER)


def find_create_user(session: Session, userinfo: dict) -> User:
    # 이메일로 검색 후 사용자가 존재하지 않으면 생성 후 반환. 사용자가 존재하면 바로 반환
    user_email = userinfo["email"]
    user = get_user_by_email(session, email=user_email)

    if not user:
        user = User.create(request=userinfo)
        create_update_user(session, user)

    return user


def get_current_user(token: TokenData) -> User:
    # 토큰으로 유저 검증
    google_userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(google_userinfo_url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()

        return user_info


@router.get("/me")
async def get_user_info(request: Request, session: Session = Depends(get_db)) -> dict:
    # 유저 정보를 받아와서 닉네임과 streak 반환
    user_info = get_current_user(token=request.headers.get("Access-Token"))
    user_email = user_info.get("email")

    user: User = get_user_by_email(session=session, email=user_email)

    return {"name": user.name, "streak": user.streak}
