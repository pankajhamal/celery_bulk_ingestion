# Celery_Bulk_Ingestion

Celery_bulk_ingestion is an asynchronous, high-performance CSV ingestion engine built with **FastAPI**, **Celery**, and **PostgreSQL**. 

Instead of inserting rows one by one, which can slow down your application and lock up the database, BulkFlow splits large CSV files into smaller "chunks" (e.g., 5,000 rows each) and processes them in parallel across multiple background workers using database bulk-insert operations.

---

## Architecture Overview

1. **Client** uploads a CSV file containing Code, symbol and name.
2. **FastAPI** reads the file, slices the rows into distinct chunks of a predefined size, and generates background jobs.
3. **Redis** acts as the message broker, storing and queuing the chunk insert jobs.
4. **Celery Workers** pull the chunks from the queue and perform efficient bulk SQL operations directly into **PostgreSQL**.

## Architecture Flow
```mermaid
flowchart TD
    A[Client / Browser] -->|1. Upload CSV File| B(FastAPI Application)
    B -->|2. Slice Rows into Chunks| B
    B -->|3. Dispatch Tasks| C[Redis Message Broker]
    B -.->|4. Return 202 Accepted + Task IDs| A

    subgraph Background Workers
        C -->|5. Fetch Tasks| D[Celery Worker Cluster]
        D -->|6. Execute Bulk Insert with ON CONFLICT DO NOTHING| E[(PostgreSQL Database)]
    end

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