from fastapi import FastAPI, HTTPException, Request
from pydantic import ValidationError
from data_model import DataModel
from llm import get_all
from custom_error import DuplicateError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request, response_class=HTMLResponse):
  return templates.TemplateResponse(request=request,
                                    name="index.html",
                                    context={"name": "Abhishek"})


@app.get("/itinerary/create", response_class=HTMLResponse)
async def create_itinerary(request: Request):
  return templates.TemplateResponse(request=request,
                                    name="show-itinerary.html")


@app.get("/itinerary", response_model=list)
def get_itinerary(data: DataModel):
  try:
    it, gl = get_all({
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
    return {
        "sucess": True,
        "it-id": str(data.id),
        "itenary": it,
        "guideline": gl
    }
  except FileNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))

  except DuplicateError as e:
    raise HTTPException(status_code=400, detail=str(e))

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8080)
