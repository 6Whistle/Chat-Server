from dataclasses import dataclass
from pydantic import BaseModel

class Response(BaseModel):
    answer: str