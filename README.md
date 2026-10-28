# Personal Expense Tracker API

## Deskripsi
Personal Expense Tracker API adalah backend untuk mencatat pemasukan dan pengeluaran pribadi. API ini menyediakan fitur CRUD transaksi, filter transaksi, dan ringkasan keuangan.

## Teknologi
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pytest
- Git

## Fitur
- Membuat transaksi pemasukan dan pengeluaran
- Menampilkan seluruh transaksi
- Menampilkan detail transaksi
- Memperbarui dan menghapus transaksi
- Memfilter transaksi berdasarkan jenis dan tanggal
- Menghitung total pemasukan, total pengeluaran, dan saldo
- Memvalidasi data transaksi

## Instalasi

Buat virtual environment dan aktifkan sesuai sistem operasi.

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

## Menjalankan aplikasi

```bash
uvicorn app.main:app --reload
```

Buka dokumentasi API di http://127.0.0.1:8000/docs.

## Menjalankan unit test

```bash
python -m pytest -v
```

## Struktur arsitektur

- `models.py`: model database
- `schemas.py`: validasi request dan response
- `repository.py`: kontrak repository dan akses database
- `services.py`: aturan bisnis
- `main.py`: endpoint API
- `tests/test_api.py`: pengujian endpoint

## Prinsip desain

Project memisahkan tanggung jawab antara endpoint, aturan bisnis, dan akses database. Kontrak repository menggunakan `Protocol` agar service tidak bergantung langsung pada implementasi penyimpanan tertentu.

Git digunakan untuk mencatat perubahan kode secara bertahap.