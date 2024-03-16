from typing import List
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import User, Test, Question


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
