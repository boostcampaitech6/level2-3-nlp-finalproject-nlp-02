import json
import yaml
import psycopg2
from datetime import datetime, timedelta


def create_date(data):
    start_date = datetime(2024, 3, 21)
    num_values = len(data)
    interval = timedelta(days=1)
    date_series = [start_date + i * interval for i in range(num_values)]

    return date_series

def load_config(filename):
    with open(filename, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config("/home/dashic/level2-3-nlp-finalproject-nlp-02/config.yaml")
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

qdata_path = '/home/dashic/level2-3-nlp-finalproject-nlp-02/data/generated_question.json'
with open(qdata_path, 'r') as f:
    data = json.load(f)
    date = create_date(data)
    for idx, line in enumerate(data):
        today = date[idx]
        q1 = line['Q1']
        q2 = line['Q2']
        q3 = line['Q3']

        query = "INSERT INTO questions (date, q1, q2, q3) VALUES (%s, %s, %s, %s)"
        data = (today, q1, q2, q3)
        cur.execute(query, data)
        conn.commit()

cur.close()
conn.close()