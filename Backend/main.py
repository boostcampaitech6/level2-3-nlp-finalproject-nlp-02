from typing import List

import uvicorn
import yaml
from auth_router import router as auth_router
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from test_router import router as test_router

app = FastAPI()
app.include_router(auth_router, prefix="/api")
app.include_router(test_router, prefix="/api")

# load config.yaml
def load_config(filename):
    with open(filename, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


config = load_config("../config.yaml")
google_config = config.get("google")
app.add_middleware(
    SessionMiddleware, secret_key=google_config.get("middleware_secret_key")
)


# 기본 연결 확인
@app.get("/")
def connection_test_handler():
    return {"Dunning": "Kruger"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
