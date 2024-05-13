from fastapi import APIRouter

from fastapi.middleware.cors import CORSMiddleware
from app.api.common.model.request import Request
from app.api.titanic.service.titanic_service import TitanicService
from app.api.common.model.response import Response

router = APIRouter()

@router.post("/chat/titanic")
async def titanic(req:Request):
    TitanicService().process()
    return Response(answer="The count of survived people is 342.")