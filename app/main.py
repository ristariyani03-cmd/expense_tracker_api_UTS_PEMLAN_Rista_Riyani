
from contextlib import asynccontextmanager
from datetime import date
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Transaction
from app.repository import SQLAlchemyTransactionRepository
from app.schemas import (
    SummaryResponse,
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from app.services import TransactionService


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Personal Expense Tracker API",
    description="Backend untuk pencatatan keuangan pribadi",
    version="1.0.0",
    lifespan=lifespan,
)


def get_service(db: Session = Depends(get_db)) -> TransactionService:
    repository = SQLAlchemyTransactionRepository(db)
    return TransactionService(repository)


@app.get("/")
def home():
    return {"message": "Personal Expense Tracker API is running"}


@app.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=201,
)
def create_transaction(
    data: TransactionCreate,
    service: TransactionService = Depends(get_service),
):
    return service.create_transaction(data.model_dump())


@app.get(
    "/transactions",
    response_model=list[TransactionResponse],
)
def get_transactions(
    transaction_type: Literal["income", "expense"] | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    service: TransactionService = Depends(get_service),
):
    try:
        return service.get_transactions(
            transaction_type, start_date, end_date
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_service),
):
    transaction = service.get_transaction(transaction_id)

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")

    return transaction


@app.put(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse,
)
def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    service: TransactionService = Depends(get_service),
):
    try:
        transaction = service.update_transaction(
            transaction_id,
            data.model_dump(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")

    return transaction


@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_service),
):
    deleted = service.delete_transaction(transaction_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")

    return {"message": "Transaksi berhasil dihapus"}


@app.get("/summary", response_model=SummaryResponse)
def get_summary(
    service: TransactionService = Depends(get_service),
):
    return service.get_summary()
