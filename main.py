from typing import List
from datetime import datetime
from tempfile import NamedTemporaryFile
import uuid
import os

from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware

from database.connection import get_db
from database.repository import (
    get_user_by_email,
    create_user,
    create_test,
    get_questions_by_date,
    get_personal_tests,
)
from database.orm import User, Test, Question
from schema.response import (
    TestSchema,
    QuestionSchema,
    TestListSchema,
)
from schema.request import CreateTestRequest
import requests
import shutil

import uvicorn
import yaml
app = FastAPI()

oauth = OAuth()

# load config.yaml
def load_config(filename):
    with open(filename, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config
config = load_config("config.yaml")
google_config = config.get("google")
app.add_middleware(SessionMiddleware, secret_key=google_config.get('middleware_secret_key'))

# google
oauth.register(
    name="google",
    client_id=google_config.get('client_id'),
    client_secret=google_config.get('client_secret'),
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


async def save_temp_file(file,):
    with NamedTemporaryFile("wb", suffix=".wav", delete=False) as tempfile:
        tempfile.write(file.read())

        return tempfile.name


@app.post("/test")
async def upload_temp(file: UploadFile,):
    path = await save_temp_file(file.file)
    
    #file_path = f"/Users/kimdonghyeon/boostcamp/Mopic/level2-3-nlp-finalproject-nlp-02/{file.filename}"
        # 파일을 저장
    # with open(upload_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)
    response = requests.post("http://localhost:8001/run_inference/", json={"data": path})
    output_json = response.json()
    
    return {"success":output_json}


async def save_file(file, path):
    wavfile = await file.read()
    name = f"{str(uuid.uuid4())}.wav"
    
    with open(os.path.join(path, name), "wb") as f:
        f.write(wavfile)

    return "{path}/{name}"


@app.post("/save")
async def upload_db(
    file,
    request: CreateTestRequest,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    UPLOAD_DIR = "/upload/{user.id}"

    path = await save_file(file, UPLOAD_DIR)
    test: Test | None = Test.create(request=request, user=user, filepath=path)
    test: Test = create_test(session=session, test=test)


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


@app.get("/me/result", status_code=200)
def get_result_handler(
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tests: List[Test] = get_personal_tests(session=session, user=user)

    return TestListSchema(tests=[TestSchema.from_orm(test) for test in tests])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
