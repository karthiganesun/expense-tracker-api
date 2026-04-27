from pydantic import BaseModel,Field
from datetime import date
from typing import Optional,Dict,List


class UserCreate(BaseModel):
   
    title: str
    # amount: float= Field(gt=0)
    amount: float
    category: str
    date: date
    notes: Optional[str]

class UserResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    date: date
    notes: Optional[str]


    class Config:
        from_attributes = True


class CategoryBreakdown(BaseModel):
    category: str
    amount: float 

class ExpenseResponse(BaseModel):
    Total_amount: float
    category_breakdown: list[CategoryBreakdown]

   