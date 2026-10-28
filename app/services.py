
from datetime import date

from app.models import Transaction
from app.repository import TransactionRepository


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def create_transaction(self, data: dict) -> Transaction:
        if data["amount"] <= 0:
            raise ValueError("Nominal harus lebih besar dari nol")

        return self.repository.create(data)

    def get_transactions(
        self,
        transaction_type: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Transaction]:
        if start_date and end_date and start_date > end_date:
            raise ValueError("Tanggal awal tidak boleh melewati tanggal akhir")

        return self.repository.get_all(
            transaction_type, start_date, end_date
        )

    def get_transaction(self, transaction_id: int) -> Transaction | None:
        return self.repository.get_by_id(transaction_id)

    def update_transaction(
        self, transaction_id: int, data: dict
    ) -> Transaction | None:
        transaction = self.repository.get_by_id(transaction_id)

        if transaction is None:
            return None

        if "amount" in data and data["amount"] <= 0:
            raise ValueError("Nominal harus lebih besar dari nol")

        return self.repository.update(transaction, data)

    def delete_transaction(self, transaction_id: int) -> bool:
        transaction = self.repository.get_by_id(transaction_id)

        if transaction is None:
            return False

        self.repository.delete(transaction)
        return True

    def get_summary(self) -> dict:
        return self.repository.get_summary()
