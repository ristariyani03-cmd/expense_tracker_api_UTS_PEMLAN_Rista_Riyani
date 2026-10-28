
from datetime import date

from sqlalchemy import Column, Date, Float, Integer, String

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(10), nullable=False)
    category = Column(String(50), nullable=False)
    transaction_date = Column(Date, default=date.today, nullable=False)
