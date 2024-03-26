import schedule
import time
import yaml
import psycopg2


def load_config(filename):
    with open(filename, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def execute_query():
    config = load_config("../config.yaml")
    db_config = config.get("database")

    host_ip = db_config["dbname"][32:47]
    db = db_config["dbname"][48:55]
    user = db_config["username"]
    password = db_config["password"]

    conn = psycopg2.connect(
        host=host_ip, 
        database=db, 
        user=user, 
        password=password
    )

    cur = conn.cursor()

    reset_streak = 0
    is_done = False
    
    # 데일리 문제 안 푼 유저 streak 초기화
    query_streak = "UPDATE users SET streak=%s WHERE is_done=%s"
    values = (reset_streak, is_done)
    cur.execute(query_streak, values)

    # 매일 밤 users 테이블 is_done 초기화
    query_done = "UPDATE users SET is_done=%s"
    values = (is_done)
    cur.execute(query_done, values)

    conn.commit()
    conn.close()

# 매일 오전 12시 쿼리 실행
schedule.every().day.at("00:00").do(execute_query)

while True:
    schedule.run_pending()
    time.sleep(1)
