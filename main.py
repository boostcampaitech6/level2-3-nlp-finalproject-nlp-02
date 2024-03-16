from typing import List
from datetime import datetime

from fastapi import FastAPI, Body, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware

from database.connection import get_db
from database.repository import (
    get_user_by_user_id,
    get_user_by_email,
    create_user,
    update_user,
    delete_user,
    create_test,
    get_questions_by_date,
    get_tests,
)
from database.orm import User, Test, Question
from schema.response import UserSchema, TestSchema, QuestionSchema, TestListSchema
from schema.request import CreateUserRequest, CreateTestRequest


app = FastAPI()

oauth = OAuth()

app.add_middleware(SessionMiddleware, secret_key="###YOUR SECRET_KEY ###")

# google
oauth.register(
    name="google",
    client_id="### YOUR GCP CLIENT ID ###",
    client_secret="### YOUR GCP CLIENT SECRET ID ###",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)

# 기본 연결 확인
@app.get("/")
def connection_test_handler():
    return {"Dunning": "Kruger"}


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route("/auth")
async def auth(request: Request, session: Session = next(get_db())):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token["userinfo"]

    tempuser: User = User.create(request=userinfo)
    user: User | None = get_user_by_email(session=session, email=tempuser.email)

    if not user:
        create_user(session=session, user=tempuser)

    request.session["user_info"] = userinfo

    return RedirectResponse(url="/done", status_code=303)


@app.get("/me")
async def get_current_user(request: Request, session: Session = Depends(get_db)):
    user_info = request.session.get("user_info")

    if user_info:
        return get_user_by_email(session=session, email=user_info["email"])

    return {"message": "no session"}

    
# 테스트 결과 db 업로드
@app.post("/test/end", status_code=201)
def create_test_handler(
    request: CreateTestRequest,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TestSchema:
    ### '해당 로그인 한 유저 id 가져오기' ###
    test: Test | None = Test.create(request=request)
    test: Test = create_test(session=session, test=test)

    return TestSchema.from_orm(test)


# 오늘 날짜로 문제 받아오기
@app.get("/test", status_code=200)
def get_question_handler(session: Session = Depends(get_db),) -> QuestionSchema:
    today: datetime.date = datetime.today()
    questions: Question | None = get_questions_by_date(
        session=session, date=today.strftime("%Y-%m-%d")
    )

    if questions:
        return QuestionSchema.from_orm(questions)
    raise HTTPException(status_code=404, detail="Question Not Found")


# 테스트 결과 불러오기
@app.get("/result", status_code=200)
def get_result_handler(session: Session = Depends(get_db),) -> TestListSchema:
    tests: List[Test] = get_tests(session=session)

    return TestListSchema(tests=[TestSchema.from_orm(test) for test in tests])
