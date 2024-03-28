import psycopg2
import yaml


def load_config(filename):
    with open(filename, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def execute_query():
    config = load_config("../../config.yaml")
    db_config = config.get("database")

    host_ip = db_config["dbname"][32:47]
    db = db_config["dbname"][48:55]
    user = db_config["username"]
    password = db_config["password"]

    conn = psycopg2.connect(host=host_ip, database=db, user=user, password=password)

    cur = conn.cursor()

    # 데일리 문제 안 푼 유저 streak 초기화
    cur.execute("UPDATE users SET streak=0 WHERE is_done=False")

    # 매일 밤 users 테이블 is_done 초기화
    cur.execute("UPDATE users SET is_done=False")

    conn.commit()
    cur.close()
    conn.close()


execute_query()
