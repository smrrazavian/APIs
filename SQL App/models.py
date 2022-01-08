from pydantic import BaseModel


class Numbers(BaseModel):
    divided: float
    factor: float
    result: float
    id: int
