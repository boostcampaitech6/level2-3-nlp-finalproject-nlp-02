from datetime import date

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str


class CreateTestRequest(BaseModel):
    user_id: int
    path: str
    mpr: float
    grammar: str
    coherence: str
    complexity: str
    wpm: float
    pause: float
    mlr: float
    q_num: int
    createddate: date


class CreateScoreRequest(BaseModel):
    user_id: int
    date: date
    score: str
