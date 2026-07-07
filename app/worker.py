from celery import Celery
from celery.signals import worker_process_init
from app.config import settings
from app.connection import engine, SessionLocal
from app.models import User 
from sqlalchemy import insert

celery_app = Celery(
  "tasks",
  broker=settings.REDIS_URL,
  backend=settings.REDIS_URL
)

# Force workers to only pull 1 task at a time
celery_app.conf.worker_prefetch_multipler = 1

#Acknowledge the task ONLY after it is fully finished inserting.
#If a worker crashes mid-insert, Celery will safely give the task to another worker.
celery_app.conf.task_acks_late = True

# Fork sfety step
@worker_process_init.connect
def init_worker_connection(**kwargs):
  """
  When celery forks a new worker process, dispose of the inherited connection pool and allow SQLAlchemy to establish fresh, isolated connections.
  """
  engine.dispose()
  print("Database connection pool successfully reset for worker process")


@celery_app.task
def insert_chunk_to_db(chunk_data: list):
  db = SessionLocal()

  try: 
    db.execute(
       insert(User),
       chunk_data
    )

    db.commit()
    return f"Inserted {len(chunk_data)} rows."
  except Exception as e:
      db.rollback()
      raise e
  finally:
     db.close() 
