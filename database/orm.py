from sqlalchemy import Boolean, Column, Integer, String, Date, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB

from schema.request import CreateUserRequest, CreateTestRequest

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_done = Column(Boolean, nullable=False)
    streak = Column(Integer, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}), name={self.name}, email={self.email}, is_done={self.is_done}, streak={self.streak}"

    @classmethod
    def create(cls, request: CreateUserRequest) -> "User":
        return cls(name=request.name, email=request.email, is_done=False, streak=0)

    def changename(self, newname) -> "User":
        self.name = newname
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
    user_id = Column(Integer, nullable=False)  # user_id
    path = Column(String, nullable=False)  # path_to_wav
    mpr = Column(Float, nullable=False)  # mispronunciation_rate
    coherence = Column(Float, nullable=False)  # coherence_level
    complexity = Column(String, nullable=False)  # complexity_analysis
    wpm = Column(Float, nullable=False)  # word_per_minute
    pause = Column(Float, nullable=False)  # pause_rate
    mlr = Column(Float, nullable=False)  # mean_length_of_run
    q_num = Column(Integer, nullable=False)  # question_number
    createdDate = Column(Date, nullable=False)  # date

    def __repr__(self):
        return f"Test user_id={self.user_id}), createdDate={self.createdDate}, q_num={self.q_num}"

    @classmethod
    def create(cls, request: CreateTestRequest, user: User, filepath: str) -> "Test":
        return cls(
            user_id=user.id,
            path=filepath,
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
