from fastapi import FastAPI
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.main_router import router
from app.api.common.model.request import Request
from app.api.common.model.response import Response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.include_router(router)

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
    chat_model = ChatOpenAI(
        openai_api_key=os.environ["API_KEY"],
        temperature=0.1,
        max_tokens=2048,
        model_name="gpt-3.5-turbo-0613",
    )

    message = [
        SystemMessage(content="""
                      You are SQL Developer. My database is innodb mysql.
                      The database has a table named 'players' with the following columns: id, name, age.
                      The database has another table named 'teams' with the following columns: id, name, player_id.
                      """, type="system"),
        HumanMessage(content="What is the SQL query to get all players?", type="human"),
        AIMessage(content="SELECT * FROM players", type="ai"),
    ]

    print('[답변] : ', chat_model.predict_messages(message))
    return {"Hello": "World"}


@app.post("/chat/ai")
async def chat(req:Request) -> Response:
    chat_model = ChatOpenAI(
        openai_api_key=os.environ["API_KEY"],
        temperature=0.1,
        max_tokens=2048,
        model_name="gpt-3.5-turbo-0613",
    )

    return Response(answer=chat_model.predict(req.question))