import io
import os
import uuid
from datetime import date, datetime
from typing import List

import librosa
import requests
import soundfile as sf
from auth_router import get_authorized_user
from database.connection import get_db
from database.orm import Question, Score, Test, User
from database.repository import (create_test, get_questions_by_date, get_result,
                                 get_result_by_q_num, create_update_user)
from fastapi import (APIRouter, Depends, File, HTTPException,
                     UploadFile)
from schema.request import CreateTestRequest
from schema.response import QuestionSchema, ScoreSchema, TestSchema
from sqlalchemy.orm import Session

router = APIRouter()


async def save_and_process_audio(file: UploadFile, user_id: int, q_num: str) -> str:
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
    # 모델단으로 연결
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

# inference 이후 데이터 베이스에 업로드
@router.post("/test")
async def upload_test(
    file: UploadFile = File(...),
    user: User = Depends(get_authorized_user),
    session: Session = Depends(get_db),
):
    question_data = get_question_handler(session)
    q_num = file.filename.split('_')[-1].split('.')[0][-1]

    file_path = await save_and_process_audio(file, str(user.id), q_num)

    question = getattr(question_data, f"q{q_num}", "질문을 찾을 수 없음")
    output = await run_inference(file_path, question)

    test_request = CreateTestRequest(**output, user_id=user.id, path=file_path, q_num=int(q_num), createddate=datetime.now().strftime("%Y-%m-%d"))
    test: Test | None = Test.create(request=test_request)
    test = create_test(session=session, test=test)

    if q_num == 3:
        user.addstreak()
        user.done()
        create_update_user()

    return TestSchema.from_orm(test)


@router.get("/me/result/{date}")
async def get_result_by_date(
    date: date, user: User = Depends(get_authorized_user), session: Session = Depends(get_db)
):
    score: Score = get_result(session=session, date=date, user=user)

    return ScoreSchema.from_orm(score)


@router.get("/me/result/{date}/{q_num}")
async def get_result_by_question(
    date: date, q_num: int, user: User = Depends(get_authorized_user), session: Session = Depends(get_db)
):
    test: Test = get_result_by_q_num(session=session, date=date, user=user, q_num=q_num)

    return TestSchema.from_orm(test)
