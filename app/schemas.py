
from datetime import date

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class TransactionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    transaction_type: Literal["income", "expense"]
    category: str = Field(min_length=1, max_length=50)
    transaction_date: date


class TransactionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    amount: float | None = Field(default=None, gt=0)
    transaction_type: Literal["income", "expense"] | None = None
    category: str | None = Field(default=None, min_length=1, max_length=50)
    transaction_date: date | None = None


class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    transaction_type: str
    category: str
    transaction_date: date

    model_config = ConfigDict(from_attributes=True)


class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float
