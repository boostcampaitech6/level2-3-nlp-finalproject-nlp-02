from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://ID:PW@IPADDRESS/DBNAME"

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
