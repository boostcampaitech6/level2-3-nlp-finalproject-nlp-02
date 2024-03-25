from datetime import date
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import Question, Test, User, Score


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.scalar(select(User).where(User.email == email))


def create_user(session: Session, user: User) -> User:
    session.add(instance=user)
    session.commit()  # db save
    session.refresh(instance=user)  # db_read
    return user


def update_user(session: Session, user: User) -> User:
    session.add(instance=user)
    session.commit()  # db save
    session.refresh(instance=user)
    return user


def create_test(session: Session, test: Test) -> Test:
    session.add(instance=test)
    session.commit()
    session.refresh(instance=test)
    return test


def get_questions_by_date(session: Session, date: date) -> Question | None:
    return session.scalar(select(Question).where(Question.date == date))


def get_personal_tests(session: Session, user: User) -> List[Test]:
    return list(session.scalars(select(Test).where(Test.user_id == user.id)))


def get_result(session: Session, date: date, user: User) -> Score:
    return session.scalar(
        select(Score).where(Score.date == date, Score.user_id == user.id)
    )


def get_result_by_q_num(session: Session, date: date, user: User, q_num: int) -> Test:
    return session.scalar(
        select(Test).where(
            Test.date == date, Test.user_id == user.id, Test.q_num == q_num
        )
    )
