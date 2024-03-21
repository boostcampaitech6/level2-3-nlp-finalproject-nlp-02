import os
import uuid
from datetime import datetime, date
from tempfile import NamedTemporaryFile
from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Request
from sqlalchemy.orm import Session

from auth_router import get_current_user, get_current
from database.connection import get_db
from database.orm import Question, Test, User
from database.repository import (create_test, get_personal_tests,
                                 get_questions_by_date, get_user_by_email, get_result)
from schema.request import CreateTestRequest
from schema.response import QuestionSchema, TestListSchema, TestSchema

router = APIRouter()


async def save_temp_file(file,):
    with NamedTemporaryFile("wb", suffix=".wav", delete=False) as tempfile:
        tempfile.write(file.read())

        return tempfile.name


async def save_file(file, path):
    wavfile = await file.read()
    name = f"{str(uuid.uuid4())}.wav"

    with open(os.path.join(path, name), "wb") as f:
        f.write(wavfile)

    return "{path}/{name}"


async def run_inference(path: str):
    response = requests.post("http://localhost:8001/run_inference/", json={"data": path})
    return response.json()

# @router.post("/save")
# async def upload_db(
#     file,
#     request: CreateTestRequest,
#     session: Session = Depends(get_db),
#     user: User = Depends(get_current_user),
# ):
#     UPLOAD_DIR = "/upload/{user.id}"

#     path = await save_file(file, UPLOAD_DIR)
#     test: Test | None = Test.create(request=request, user=user, filepath=path)
#     test: Test = create_test(session=session, test=test)


@router.post("/test")
async def upload_temp(
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    ):

    path = await save_temp_file(file.file)
    output = await run_inference(path)
    UPLOAD_DIR = "/upload/{user.id}"
    request = CreateTestRequest
    request.user_id = user.id
    request.path = path
    request.mpr = output['mpr']
    request.grammar = output['grammar']
    request.coherence = output['coherence']
    request.complexity = output['complexity']
    request.pause = output['pause']
    request.wpm = output['wpm']
    request.mlr = output['mlr']
    request.q_num = 1
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    request.createdDate = formatted_date
    print(request)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    test: Test | None = Test.create(request = request)
    test: Test = create_test(session=session, test=test)
    return test



# 오늘 날짜로 문제 받아오기
@router.get("/test", status_code=200)
def get_question_handler(session: Session = Depends(get_db),) -> QuestionSchema:
    today: datetime.date = datetime.today()
    questions: Question | None = get_questions_by_date(
        session=session, date=today.strftime("%Y-%m-%d")
    )

    if questions:
        return QuestionSchema.from_orm(questions)
    raise HTTPException(status_code=404, detail="Question Not Found")


@router.get("/me/result", status_code=200)
def get_result_handler(
    session: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    tests: List[Test] = get_personal_tests(session=session, user=user)

    return TestListSchema(tests=[TestSchema.from_orm(test) for test in tests])


@router.get("/me/result/{date}")
async def get_result_by_date(request: Request, date: date, session: Session = Depends(get_db), ):
    user_info = get_current(token=request.headers.get("access_token"))
    user_email = user_info.get("email")

    user: User = get_user_by_email(session=session, email=user_email)
    test: Test = get_result(session=session, date=date, user=user)

    return TestSchema.from_orm(test)