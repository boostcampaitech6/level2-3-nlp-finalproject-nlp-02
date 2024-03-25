from datetime import date
from typing import List

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    is_done: bool
    streak: int
    email: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserListSchema(BaseModel):
    users: List[UserSchema]


class TestSchema(BaseModel):
    id: int
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

    class Config:
        orm_mode = True
        from_attributes = True


class TestListSchema(BaseModel):
    tests: List[TestSchema]


class QuestionSchema(BaseModel):
    id: int
    date: date
    q1: str
    q2: str
    q3: str
    q1_wav: str
    q2_wav: str
    q3_wav: str

    class Config:
        orm_mode = True
        from_attributes = True


class QuestionListSchema(BaseModel):
    questions: List[QuestionSchema]


class ScoreSchema(BaseModel):
    id: int
    user_id: int
    date: date
    score: str

    class Config:
        orm_mode = True
        from_attributes = True
