
from datetime import date

import pytest

from app.services import TransactionService


class FakeTransactionRepository:
    def __init__(self):
        self.transactions = []
        self.next_id = 1

    def create(self, data):
        transaction = {
            **data,
            "id": self.next_id,
        }
        self.next_id += 1
        self.transactions.append(transaction)
        return transaction

    def get_all(
        self,
        transaction_type=None,
        start_date=None,
        end_date=None,
    ):
        result = self.transactions

        if transaction_type:
            result = [
                t for t in result
                if t["transaction_type"] == transaction_type
            ]

        if start_date:
            result = [
                t for t in result
                if t["transaction_date"] >= start_date
            ]

        if end_date:
            result = [
                t for t in result
                if t["transaction_date"] <= end_date
            ]

        return result

    def get_by_id(self, transaction_id):
        return next(
            (
                t for t in self.transactions
                if t["id"] == transaction_id
            ),
            None,
        )

    def update(self, transaction, data):
        transaction.update(data)
        return transaction

    def delete(self, transaction):
        self.transactions.remove(transaction)

    def get_summary(self):
        income = sum(
            t["amount"] for t in self.transactions
            if t["transaction_type"] == "income"
        )
        expense = sum(
            t["amount"] for t in self.transactions
            if t["transaction_type"] == "expense"
        )
        return {
            "total_income": income,
            "total_expense": expense,
            "balance": income - expense,
        }


@pytest.fixture
def service():
    repository = FakeTransactionRepository()
    return TransactionService(repository)


def test_create_transaction(service):
    transaction = service.create_transaction({
        "title": "Uang bulanan",
        "amount": 1000000,
        "transaction_type": "income",
        "category": "Pemasukan",
        "transaction_date": date(2026, 10, 26),
    })

    assert transaction["id"] == 1
    assert transaction["amount"] == 1000000


def test_reject_invalid_amount(service):
    with pytest.raises(ValueError):
        service.create_transaction({
            "title": "Belanja",
            "amount": -10000,
            "transaction_type": "expense",
            "category": "Makanan",
            "transaction_date": date(2026, 10, 26),
        })


def test_reject_invalid_date_range(service):
    with pytest.raises(ValueError):
        service.get_transactions(
            start_date=date(2026, 10, 31),
            end_date=date(2026, 10, 1),
        )


def test_delete_missing_transaction(service):
    result = service.delete_transaction(999)

    assert result is False
