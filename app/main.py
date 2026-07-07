from fastapi import FastAPI
from io import StringIO
from fastapi import UploadFile, File
import csv
from app.worker import insert_chunk_to_db

app = FastAPI()

CHUNK_SIZE = 5000 # Adjust based on your server memeory and DB performance

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
  #Read the file content
  contents = await file.read()
  csv_file = StringIO(contents.decode('UTF-8'))
  reader = csv.DictReader(csv_file)

  chunk = []
  task_ids = []

  for row in reader:
    #Row expected to look like: {"name": "Pankaj Hamal", "email:" "pankajhamal0@gmail.com"}
    chunk.append({
      "name": row.get("name"),
      "email": row.get("email")
    })

    #Once we hit our chunk size limit, send it to a celery worker

    if len(chunk) >= CHUNK_SIZE:
      task = insert_chunk_to_db.delay(chunk)
      task_ids.append(task.id)
      chunk = [] #Reset the chunk 

    #Edge case if there are remaining chunk left
    if chunk:
      task = insert_chunk_to_db.delay(chunk)
      task_ids.append(task.id)

    return {
      "message": f"File received. Data split into {len(task_ids)} background tasks.",
      "tasks_dispatched": len(task_ids),
      "task_ids": task_ids
    }






