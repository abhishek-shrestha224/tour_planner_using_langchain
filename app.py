from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from data_model import DataModel
from custom_error import DuplicateError
from uuid import uuid4
import csv
import os

app = FastAPI()

CSV_FILE_PATH = 'data.csv'


def save_tasks_to_csv(data: DataModel) -> None:
  existing_data = []
  try:
    with open(CSV_FILE_PATH, 'r', newline='') as file:
      reader = csv.DictReader(file)
      for row in reader:
        existing_data.append({
            "first_name": row["first_name"],
            "last_name": row["last_name"]
        })
  except FileNotFoundError:
    pass

  with open(CSV_FILE_PATH, 'a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=DataModel.__annotations__.keys())

    if file.tell() == 0:
      writer.writeheader()

    if any(
        t["first_name"] == data.first_name and t["last_name"] == data.last_name
        for t in existing_data):
      raise DuplicateError(
          f"Task for {data.first_name} {data.last_name} already exists.")

    data_dict = data.model_dump()
    writer.writerow(data_dict)
    existing_data.append({
        "first_name": data.first_name,
        "last_name": data.last_name
    })


@app.get("/")
def root():
  return {"Hello": "World"}


@app.get("/get-my-plan")
def get_plan(data: DataModel):
  data.id = uuid4()
  try:
    save_tasks_to_csv(data)
    return {"success": True, "plan": {"Day-2": "Say Hello"}}

  except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))

  except DuplicateError as e:
    raise HTTPException(status_code=400, detail=str(e))

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8080)
