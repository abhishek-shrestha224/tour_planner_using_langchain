from fastapi import FastAPI, HTTPException
from typing import List
from uuid import uuid4, UUID
import csv
import os

app = FastAPI()

CSV_FILE_PATH = 'tasks.csv'


def load_tasks_from_csv() -> List[Task]:
  if not os.path.exists(CSV_FILE_PATH):
    return []

  tasks = []
  with open(CSV_FILE_PATH, newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
      row['id'] = UUID(row['id'])
      row['is_compeleted'] = row['is_compeleted'] == 'True'
      tasks.append(Task(**row))
  return tasks


def save_tasks_to_csv(tasks: List[Task]) -> None:
  with open(CSV_FILE_PATH, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=Task.__annotations__.keys())
    writer.writeheader()
    for task in tasks:
      task_dict = task.model_dump()
      task_dict['is_compeleted'] = str(task_dict['is_compeleted'])
      writer.writerow(task_dict)


@app.get("/")
def root():
  return {"Hello": "World"}


# ! Create Task


@app.post("/tasks/", response_model=Task)
def store_task(task: Task):
  task.id = uuid4()
  tasks = load_tasks_from_csv()
  tasks.append(task)
  save_tasks_to_csv(tasks)
  return task


# ! Read Tasks


@app.get("/tasks/", response_model=List[Task])
def get_all_tasks():
  return load_tasks_from_csv()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(task_id: UUID):
  tasks = load_tasks_from_csv()

  for task in tasks:
    if task.id == task_id:
      return task
  raise HTTPException(status_code=404,
                      detail=f"Task with id {task_id} not found.")


# ! Update Task


@app.put("/tasks/{param}", response_model=Task)
def edit_task_by_id(param: UUID, new_task: Task):
  tasks = load_tasks_from_csv()

  for i, task in enumerate(tasks):
    if task.id == param:
      updated_task = task.model_copy(update=new_task.model_dump(
          exclude_unset=True))
      tasks[i] = updated_task
      save_tasks_to_csv(tasks)
      return updated_task

  raise HTTPException(status_code=404,
                      detail=f"Task with id {param} not found.")


# ! Delete Task


@app.delete("/tasks/{param}", response_model=Task)
def delete_task_by_id(param: UUID):
  tasks = load_tasks_from_csv()

  for i, task in enumerate(tasks):
    if task.id == param:
      deleted_task = tasks.pop(i)
      save_tasks_to_csv(tasks)
      return deleted_task

  raise HTTPException(status_code=404,
                      detail=f"Task with id {param} not found.")


@app.delete("/tasks/")
def delete_all_tasks():
  save_tasks_to_csv([])
  return {"message": "Tasks Cleared Sucessfully."}
