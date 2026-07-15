# Celery_Bulk_Ingestion

<div align="center">
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Celery-378140?style=for-the-badge&logo=celery&logoColor=white" alt="Celery" />
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
</div>

Celery_bulk_ingestion is an asynchronous, high-performance CSV ingestion engine built with **FastAPI**, **Celery**, and **PostgreSQL**.

Instead of inserting rows one by one, which can slow down your application and lock up the database, BulkFlow splits large CSV files into smaller "chunks" (e.g., 5,000 rows each) and processes them in parallel across multiple background workers using database bulk-insert operations.

---

## Architecture Overview

1. **Client** uploads a CSV file containing Code, symbol and name.
2. **FastAPI** reads the file, slices the rows into distinct chunks of a predefined size, and generates background jobs.
3. **Redis** acts as the message broker, storing and queuing the chunk insert jobs.
4. **Celery Workers** pull the chunks from the queue and perform efficient bulk SQL operations directly into **PostgreSQL**.

---

## Tech Stack

- **Framework:** FastAPI
- **Task Queue:** Celery
- **Message Broker & Results Backend:** Redis
- **Database:** PostgreSQL (using `psycopg2` for bulk execution)
- **Language:** Python 3.10+

---

## Getting Started

### Prerequisites

You will need Python installed

### 1. Clone the Repository & Set Up Virtual Environment

```bash
git clone https://github.com/pankajhamal/celery_bulk_ingestion.git
cd celery_bulk_ingestion

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install requirements.txt
pip install requirements.txt

# Start uvicorn server
uvicorn app.main:app --reload
````
