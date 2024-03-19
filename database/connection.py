from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import yaml

def load_config(filename):
    with open(filename, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config
config = load_config("config.yaml")
db_config = config.get("database")

DATABASE_URL = db_config.get('dbname')

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
