from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from data_model import DataModel
from llm import get_itinerary
from custom_error import DuplicateError
from uuid import uuid4, UUID
from fastapi.responses import RedirectResponse
import csv
import json
import os

# ! ||--------------------------------------------------------------------------------||
# ! ||                               Read Write Fuctions                              ||
# ! ||--------------------------------------------------------------------------------||

ITINERARY_PATH = "itinerary.json"
USER_PATH = "user_data.csv"


def save_user(data: DataModel) -> None:
  existing_data = []
  try:
    with open(USER_PATH, 'r', newline='') as file:
      reader = csv.DictReader(file)
      for row in reader:
        existing_data.append({
            "first_name": row["first_name"],
            "last_name": row["last_name"]
        })
  except FileNotFoundError:
    pass

  with open(USER_PATH, 'a', newline='') as file:
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


def load_all_itinerary():
  try:
    with open(ITINERARY_PATH, 'r') as f:
      loaded_data = json.load(f)
    return loaded_data
  except FileNotFoundError:
    pass
  except json.JSONDecodeError:
    raise ValueError("Error decoding JSON from the file.")
  except KeyError as e:
    raise e


def save_itinerary(id, body):
  try:
    list_dict = load_all_itinerary()
    list_dict[id] = body
    with open(ITINERARY_PATH, 'w') as f:
      json.dump(list_dict, f, indent=4)
  except FileNotFoundError:
    pass
  except json.JSONDecodeError:
    raise ValueError("Error decoding JSON from the file.")
  except KeyError as e:
    raise e


def load_itinerary_by_id(id):
  try:
    with open(ITINERARY_PATH, 'r') as f:
      loaded_data = json.load(f)
    if id not in loaded_data:
      raise KeyError(f"List ID {id} not found")
    result = loaded_data[id]
    return result
  except FileNotFoundError:
    pass
  except json.JSONDecodeError:
    raise ValueError("Error decoding JSON from the file.")
  except KeyError as e:
    raise e


app = FastAPI()


@app.get("/")
def root():
  return {"Hello": "World"}


@app.post("/itinerary/create")
def create_itinerary(data: DataModel):
  data.id = uuid4()
  try:
    save_user(data)
    itinerary = get_itinerary({
        "full_name": data.first_name + " " + data.last_name,
        "country_of_origin": data.country_of_origin,
        "occupation": data.occupation,
        "main_purpose_of_visit": data.main_purpose_of_visit,
        "travel_budget": data.travel_budget,
        "duration_of_visit": data.duration_of_visit,
        "food_preferences": data.food_preferences,
        "preferred_attractions": data.preferred_attractions,
        "number_of_people_travelling": data.number_of_people_travelling,
        "special_activities_interested": data.special_activities_interested,
        "transportation_preferences": data.transportation_preferences,
        "accommodation_preferences": data.accommodation_preferences,
        "interested_places": data.interested_places,
        "weather_preference": data.weather_preference,
        "from_month": data.from_month,
        "to_month": data.to_month
    })
    save_itinerary(str(data.id), itinerary)
    return {"sucess": True, "it-id": str(data.id), "plan": itinerary}
    # return RedirectResponse(url=f"/itinerary/{str(data.id)}")
  except FileNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))

  except DuplicateError as e:
    raise HTTPException(status_code=400, detail=str(e))

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.get("/itinerary/{param}", response_model=list)
def get_itinerary_by_id(param: str):
  try:
    itinerary = load_itinerary_by_id(param)
    return itinerary
  except KeyError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8080)
