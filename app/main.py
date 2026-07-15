from fastapi import FastAPI
from io import StringIO
from fastapi import UploadFile, File, HTTPException
import csv
from app.worker import insert_chunk_to_db
from app.connection import Base, engine

app = FastAPI()

Base.metadata.create_all(engine)


CHUNK_SIZE = 10 # Adjust based on your server memeory and DB performance

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    #Read the file content
    contents = await file.read()
    csv_file = StringIO(contents.decode('UTF-8'))
    reader = csv.DictReader(csv_file)

    if not reader.fieldnames or "Code" not in reader.fieldnames or "Symbol" not in reader.fieldnames or "Name" not in reader.fieldnames:
      raise HTTPException(
          status_code = 400,
          detail = "Invalid CSV format. Missing 'code', 'symbol, or 'name' header columns."
      )

    chunk = []
    task_ids = []

    for row in reader:

      code = row.get("Code")
      symbol = row.get("Symbol")
      name = row.get("Name")

      cleaned_code = code.strip().upper() if code else None
      cleaned_symbol = symbol.strip().upper() if symbol else None
      cleaned_name = symbol.strip().upper() if name else None

      if not cleaned_code or not cleaned_symbol:
        continue #Code and Name are required
      

      chunk.append({
        "code": cleaned_code,
        "symbol": cleaned_symbol,
        "name": cleaned_name
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






