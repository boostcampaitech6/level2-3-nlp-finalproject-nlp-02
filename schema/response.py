from typing import List
from datetime import date

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    nickname: str
    is_done: bool
    streak: int

    class Config:
        orm_mode = True


class UserListSchema(BaseModel):
    users: List[UserSchema]


class TestSchema(BaseModel):
    id: int
    user_id: int
    path: str
    result: dict
    q_num: int
    createdDate: date

    class Config:
        orm_mode = True


class TestListSchema(BaseModel):
    tests: List[TestSchema]


class QuestionSchema(BaseModel):
    id: int
    date: str
    q1: str
    q2: str
    q3: str

    class Config:
        orm_mode = True


class QuestionListSchema(BaseModel):
    questions: List[QuestionSchema]
