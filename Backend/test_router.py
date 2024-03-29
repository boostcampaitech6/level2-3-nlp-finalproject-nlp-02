import io
import os
import uuid
from datetime import date, datetime
from typing import List

import librosa
import requests
import soundfile as sf
from auth_router import get_current_user, find_create_user
from database.connection import get_db
from database.orm import Question, Score, Test, User
from database.repository import (create_test, get_questions_by_date, get_result,
                                 get_result_by_q_num, get_user_by_email)
from fastapi import (APIRouter, Depends, File, HTTPException, Request,
                     UploadFile, status)
from schema.request import CreateTestRequest
from schema.response import QuestionSchema, ScoreSchema, TestSchema
from sqlalchemy.orm import Session

router = APIRouter()


async def save_and_process_audio(file: UploadFile, user_id: str, q_num: str) -> str:
    # 파일 저장 및 리샘플링 작업
    try:
        # 파일 저장
        name = f"{uuid.uuid4()}_{q_num}.wav"
        UPLOAD_DIR = f"./uploads/{user_id}/"        
        resampled_path = os.path.join(UPLOAD_DIR, name)
        os.makedirs(os.path.dirname(resampled_path), exist_ok=True)

        # 리샘플링 진행
        wav_bytes = io.BytesIO(await file.read())
        y, sr = librosa.load(wav_bytes, sr=44100)
        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=16000)
        sf.write(resampled_path, y_resampled, 16000)

        return resampled_path
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {e}")


async def run_inference(path: str, question: str):
    response = requests.post(
        "http://localhost:8001/run_inference/",
        json={"data": path, "question": question},
    )
    return response.json()

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
    requestsss: Request,
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
    question_data: QuestionSchema = Depends(get_question_handler),
):
    user_info = get_current_user(token=requestsss.headers.get("Access-Token"))
    user_email = user_info.get("email")

    user: User = get_user_by_email(session=session, email=user_email)

    q_num = file.filename[-5]
    q_num_question_mapping = {
        "1": question_data.q1,
        "2": question_data.q2,
        "3": question_data.q3,
    }

    file_path = await save_and_process_audio(file, user.id, q_num)
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
    request.createddate = formatted_date

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    test: Test | None = Test.create(request=request)
    test: Test = create_test(session=session, test=test)
    return test


@router.post("/test_q3")
async def upload_test1(
    requestsss: Request,
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
    question_data: QuestionSchema = Depends(get_question_handler),
):
    user_info = get_current_user(token=requestsss.headers.get("Access-Token"))
    user_email = user_info.get("email")

    user: User = get_user_by_email(session=session, email=user_email)

    q_num = file.filename[-5]

    q_num_question_mapping = {
        "1": question_data.q1,
        "2": question_data.q2,
        "3": question_data.q3,
    }

    file_path = await save_and_process_audio(file, user.id, q_num)
    # question = question_data.q1
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
    request.createddate = formatted_date

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    test: Test | None = Test.create(request=request)
    test: Test = create_test(session=session, test=test)

    user.addstreak()
    user.done()


    return test


@router.get("/me/result/{date}")
async def get_result_by_date(
    request: Request, date: date, session: Session = Depends(get_db)
):
    user_info = get_current_user(token=request.headers.get("Access-Token"))
    user_email = user_info.get("email")

    user: User = get_user_by_email(session=session, email=user_email)
    score: Score = get_result(session=session, date=date, user=user)

    return ScoreSchema.from_orm(score)


@router.get("/me/result/{date}/{q_num}")
async def get_result_by_question(
    request: Request, date: date, q_num: int, session: Session = Depends(get_db)
):
    user_info = get_current_user(token=request.headers.get("Access-Token"))
    user_email = user_info.get("email")

    user: User = get_user_by_email(session=session, email=user_email)
    test: Test = get_result_by_q_num(session=session, date=date, user=user, q_num=q_num)

    return TestSchema.from_orm(test)
