from fastapi import APIRouter

from fastapi.middleware.cors import CORSMiddleware
from app.api.common.model.request import Request
from app.api.titanic.service.titanic_service import TitanicService
from app.api.common.model.response import Response

router = APIRouter()

@router.post("/chat/titanic")
async def titanic(req:Request):
    service = TitanicService()
    service.preprocess()
    return Response(answer=f"The accuracy of {req.question} Titanic model is {service.learning(service.modeling(req.question), req.question)}%")