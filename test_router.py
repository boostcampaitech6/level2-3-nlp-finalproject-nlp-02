import os
import uuid
from datetime import datetime
from tempfile import NamedTemporaryFile
from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from auth_router import get_current_user
from database.connection import get_db
from database.orm import Question, Test, User
from database.repository import (create_test, get_personal_tests,
                                 get_questions_by_date)
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


@router.post("/save")
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


@router.post("/test")
async def upload_temp(file: UploadFile,):
    path = await save_temp_file(file.file)
    response = requests.post(
        "http://localhost:8001/run_inference/", json={"data": path}
    )
    output_json = response.json()

    return {"success": output_json}


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