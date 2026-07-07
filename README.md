# celer_bulk_ingestion

# BulkFlow

BulkFlow is an asynchronous, high-performance CSV ingestion engine built with **FastAPI**, **Celery**, and **PostgreSQL**. 

Instead of inserting rows one by one, which can slow down your application and lock up the database, BulkFlow splits large CSV files into smaller "chunks" (e.g., 5,000 rows each) and processes them in parallel across multiple background workers using database bulk-insert operations.

---

## Architecture Overview

1. **Client** uploads a CSV file containing user names and emails.
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

You will need Python installed, along with Docker to run your database and message broker easily.

### 1. Clone the Repository & Set Up Virtual Environment

```bash
git clone https://github.com/pankajhamal/celery_bulk_ingestion.git
cd bulkflow

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate