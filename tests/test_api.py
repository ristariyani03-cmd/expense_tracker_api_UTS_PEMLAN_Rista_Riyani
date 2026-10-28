
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Personal Expense Tracker API is running"
    )


def test_create_transaction(client):
    response = client.post(
        "/transactions",
        json={
            "title": "Uang bulanan",
            "amount": 1500000,
            "transaction_type": "income",
            "category": "Pemasukan",
            "transaction_date": "2026-10-26",
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Uang bulanan"
    assert response.json()["amount"] == 1500000


def test_reject_negative_amount(client):
    response = client.post(
        "/transactions",
        json={
            "title": "Belanja",
            "amount": -50000,
            "transaction_type": "expense",
            "category": "Makanan",
            "transaction_date": "2026-10-26",
        },
    )

    assert response.status_code == 422


def test_summary(client):
    client.post(
        "/transactions",
        json={
            "title": "Uang bulanan",
            "amount": 1000000,
            "transaction_type": "income",
            "category": "Pemasukan",
            "transaction_date": "2026-10-26",
        },
    )

    client.post(
        "/transactions",
        json={
            "title": "Makan",
            "amount": 150000,
            "transaction_type": "expense",
            "category": "Makanan",
            "transaction_date": "2026-10-26",
        },
    )

    response = client.get("/summary")

    assert response.status_code == 200
    assert response.json()["total_income"] == 1000000
    assert response.json()["total_expense"] == 150000
    assert response.json()["balance"] == 850000


def test_transaction_not_found(client):
    response = client.get("/transactions/999")

    assert response.status_code == 404


def test_filter_by_type(client):
    client.post(
        "/transactions",
        json={
            "title": "Makan",
            "amount": 50000,
            "transaction_type": "expense",
            "category": "Makanan",
            "transaction_date": "2026-10-26",
        },
    )

    response = client.get(
        "/transactions?transaction_type=expense"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["transaction_type"] == "expense"
