import os
import io
import librosa
import soundfile as sf
import uuid
from datetime import date, datetime
from tempfile import NamedTemporaryFile
from typing import List

import requests
from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile, status)
from sqlalchemy.orm import Session

from auth_router import get_current_user, get_current
from database.connection import get_db
from database.orm import Question, Test, User, Score
from database.repository import (create_test, get_personal_tests,
                                 get_questions_by_date, get_result,
                                 get_user_by_email, get_result_by_q_num)
from schema.request import CreateTestRequest
from schema.response import QuestionSchema, TestListSchema, TestSchema, ScoreSchema

router = APIRouter()


async def save_temp_file(file,):
    with NamedTemporaryFile("wb", suffix=".wav", delete=False) as tempfile:
        tempfile.write(file.read())

        return tempfile.name


async def save_file(file, user_id, q_num):
    wavfile = await file.read()
    #name = file.filename
    name = f"{str(uuid.uuid4())}_{q_num}.wav"
    target_sr = 16000
    UPLOAD_DIR = f"./uploads/{user_id}"
    #UPLOAD_DIR = "./uploads/"
    resampled_path = os.path.join(UPLOAD_DIR, name)
    #print(resampled_path)
    os.makedirs(os.path.dirname(UPLOAD_DIR), exist_ok=True)


    # BytesIO 객체 생성 및 다운샘플링
    wav_bytes = io.BytesIO(wavfile)
    y, sr = librosa.load(wav_bytes, sr=44100)
    
    # y_resampling
    y_resampled = librosa.resample(y, orig_sr = sr, target_sr = target_sr)

    # 다운샘플링된 파일 저장
    sf.write(resampled_path, y_resampled, target_sr)

    return resampled_path


async def run_inference(path: str, question: str):
    response = requests.post(
        "http://localhost:8001/run_inference/",
        json={"data": path, "question": question},
    )
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


@router.post("/test")
async def upload_temp(
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    question_data: QuestionSchema = Depends(get_question_handler),
):
    
    q_num = file.filename[-5]
 
    q_num_question_mapping = {
    "1": question_data.q1,
    "2": question_data.q2,
    "3": question_data.q3,
}
    
    file_path = await save_file(file, user.id, q_num)
    #question = question_data.q1
    question = q_num_question_mapping.get(q_num, "질문을 찾을 수 없음")
    output = await run_inference(file_path, question)

    request = CreateTestRequest
    request.user_id = user.id
    request.path = file_path
    request.mpr = output["mpr"]
    request.grammar = output["grammar"]
    request.coherence = output["coherence"]
    request.complexity = output["complexity"]
    request.pause = output["pause"]
    request.wpm = output["wpm"]
    request.mlr = output["mlr"]
    request.q_num = q_num
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    request.createdDate = formatted_date

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    test: Test | None = Test.create(request=request)
    test: Test = create_test(session=session, test=test)
    return test


@router.get("/me/result", status_code=200)
def get_result_handler(
    session: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    tests: List[Test] = get_personal_tests(session=session, user=user)

    return TestListSchema(tests=[TestSchema.from_orm(test) for test in tests])


@router.get("/me/result/{date}")
async def get_result_by_date(
    request: Request, date: date, session: Session = Depends(get_db)
):
    user_info = get_current(token=request.headers.get("Access-Token"))
    user_email = user_info.get("email")

    user: User = get_user_by_email(session=session, email=user_email)
    score: Score = get_result(session=session, date=date, user=user)

    return ScoreSchema.from_orm(score)

@router.get("/me/result/{date}/{q_num}")
async def get_result_by_question(
    request: Request, date: date, q_num: int, session: Session = Depends(get_db)
):
    user_info = get_current(token=request.headers.get("Access-Token"))
    user_email = user_info.get("email")

    user: User = get_user_by_email(session=session, email=user_email)
    test: Test = get_result_by_q_num(session=session, date=date, user=user, q_num=q_num)

    return TestSchema.from_orm(test)