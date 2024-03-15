from pydantic import BaseModel
from datetime import date


class CreateUserRequest(BaseModel):
    name: str
    email: str


class CreateTestRequest(BaseModel):
    user_id: int
    path: str
    result: dict
    q_num: int
    createdDate: date
