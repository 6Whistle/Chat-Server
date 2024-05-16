import os
from fastapi import FastAPI
import uvicorn
from example.bmi import BMI

app = FastAPI()


@app.get("/")
async def root():
    m = BMI()
    return {"answer": m.get_bmi("홍길동")}


if __name__ == "__main__":
    uvicorn.run(app,     host="localhost", port=8000)