import os, sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from cctv_report import CCTVReport

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    cctvReport = CCTVReport()
    return {"answer": cctvReport.save_police_position()}

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)