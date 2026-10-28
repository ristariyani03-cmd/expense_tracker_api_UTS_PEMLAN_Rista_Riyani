
from datetime import date
from typing import Protocol

from sqlalchemy.orm import Session

from app.models import Transaction


class TransactionRepository(Protocol):
    def create(self, data: dict) -> Transaction: ...
    def get_all(
        self,
        transaction_type: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Transaction]: ...
    def get_by_id(self, transaction_id: int) -> Transaction | None: ...
    def update(self, transaction: Transaction, data: dict) -> Transaction: ...
    def delete(self, transaction: Transaction) -> None: ...
    def get_summary(self) -> dict: ...


class SQLAlchemyTransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Transaction:
        transaction = Transaction(**data)
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_all(
        self,
        transaction_type: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Transaction]:
        query = self.db.query(Transaction)

        if transaction_type is not None:
            query = query.filter(
                Transaction.transaction_type == transaction_type
            )

        if start_date is not None:
            query = query.filter(
                Transaction.transaction_date >= start_date
            )

        if end_date is not None:
            query = query.filter(
                Transaction.transaction_date <= end_date
            )

        return query.order_by(Transaction.id.desc()).all()

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        return self.db.get(Transaction, transaction_id)

    def update(self, transaction: Transaction, data: dict) -> Transaction:
        for key, value in data.items():
            setattr(transaction, key, value)

        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def delete(self, transaction: Transaction) -> None:
        self.db.delete(transaction)
        self.db.commit()

    def get_summary(self) -> dict:
        transactions = self.db.query(Transaction).all()

        total_income = sum(
            t.amount for t in transactions
            if t.transaction_type == "income"
        )

        total_expense = sum(
            t.amount for t in transactions
            if t.transaction_type == "expense"
        )

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense,
        }
