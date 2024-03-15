from typing import List
from datetime import date

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.orm import User, Test, Question


def get_user_by_user_id(session: Session, user_id: int) -> User | None:
    return session.scalar(select(User).where(User.id == user_id))


def create_user(session: Session, user: User) -> User:
    session.add(instance=user)
    session.commit()  # db save
    session.refresh(instance=user)  # db_read -> todo_id
    return user


def update_user(session: Session, user: User) -> User:
    session.add(instance=user)
    session.commit()  # db save
    session.refresh(instance=user)
    return user


def delete_user(session: Session, user_id: int) -> None:
    session.execute(delete(User).where(User.id == user_id))
    session.commit()


def create_test(session: Session, test: Test) -> Test:
    session.add(instance=test)
    session.commit()
    session.refresh(instance=test)
    return test


def get_tests(session: Session) -> List[Test]:
    return list(session.scalars(select(Test)))


def get_questions_by_date(session: Session, date: date) -> Question | None:
    return session.scalar(select(Question).where(Question.date == date))
