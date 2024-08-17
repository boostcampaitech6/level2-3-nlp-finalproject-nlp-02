from typing import List

import yaml
from auth_router import router as auth_router
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from test_router import router as test_router

#date, score 받아오는 엔드포인트 설정
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Score 

app = FastAPI()
app.include_router(auth_router, prefix="/api")
app.include_router(test_router, prefix="/api")


# load config.yaml
def load_config(filename):
    with open(filename, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config("../config.yaml")
google_config = config.get("google")
app.add_middleware(
    SessionMiddleware, secret_key=google_config.get("middleware_secret_key")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 특정 도메인을 설정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_coop_header(request, call_next):
    response = await call_next(request)
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
    return response

# 기본 연결 확인
@app.get("/")
def connection_test_handler():
    return {"Dunning": "Kruger"}

#date, score 받아오는 엔드포인트 설정
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/scores/")
def get_scores(db: Session = Depends(get_db)):
    scores = db.query(Score).all()  # 모든 Score 객체 가져오기
    return scores