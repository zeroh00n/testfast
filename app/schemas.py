from pydantic import BaseModel
from typing import List

class ProductBase(BaseModel):
    id: int
    name: str
    category: str
    price: float

    class Config:
        orm_mode = True


class RecommendationResponse(ProductBase):
    score: float


class ProductResponse(ProductBase):
    pass


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
