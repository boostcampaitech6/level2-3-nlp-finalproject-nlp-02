from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB

from schema.request import CreateUserRequest, CreateTestRequest

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    streak = Column(Integer, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}), name={self.nickname}, is_done={self.is_done}, streak={self.streak}"

    @classmethod
    def create(cls, request: CreateUserRequest) -> "User":
        return cls(nickname=request.nickname, is_done=False, streak=0)

    def changename(self, newname) -> "User":
        self.nickname = newname
        return self

    def done(self) -> "User":
        self.is_done = True
        return self

    def undone(self) -> "User":
        self.is_done = False
        return self


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    path = Column(String, nullable=False)
    result = Column(mutable_json_type(dbtype=JSONB, nested=True))
    q_num = Column(Integer, nullable=False)
    createdDate = Column(Date, nullable=False)

    def __repr__(self):
        return f"Test user_id={self.user_id}), createdDate={self.createdDate}, q_num={self.q_num}"

    @classmethod
    def create(cls, request: CreateTestRequest) -> "Test":
        return cls(
            user_id=request.user_id,
            path=request.path,
            result=request.result,
            q_num=request.q_num,
            createdDate=request.createdDate,
        )


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False)
    q1 = Column(String, nullable=False)
    q2 = Column(String, nullable=False)
    q3 = Column(String, nullable=False)

    def __repr__(self):
        return f"Q date={self.date}), q1={self.q1}, q2={self.q2}, q3={self.q3}"
