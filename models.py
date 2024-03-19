from fastapi import FastAPI

app = FastAPI()

@app.get("/get_wav_path/")
async def get_wav_path():
    # 여기에 WAV 파일의 경로를 반환하는 코드를 작성합니다.
    return {"path": "/path/to/your/wav/file.wav"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)
