from fastapi import APIRouter

from app.api.common.model.request import Request

router = APIRouter()

@router.post("/chat/titanic")
async def titanic(req:Request):
    return {"answer": "The count of survived people is 342."}