from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from enum import Enum


class DataModel(BaseModel):
  id: Optional[UUID] = None
  first_name: str
  last_name: str
  country_of_origin: str
  occupation: str
  main_purpose_of_visit: str
  travel_budget: float
  duration_of_visit: int
  preferred_attractions: Attraction
  special_activities_interested: Optional[str] = None
  number_of_people_travelling: int
  transportation_preferences: Optional[str] = None
  accommodation_preferences: Optional[str] = None
  interested_places: Optional[List[str]] = None
  weather_preference: Optional[str] = None
  month_of_visit: Optional[List[str]] = None

  class Config:
    schema_extra = {
        "example": {
            "id": "d9b1aadc-7891-4b0e-a7d4-59bc6f8b8e9d",
            "first_name": "John",
            "last_name": "Doe",
            "country_of_origin": "China",
            "occupation": "Software Engineer",
            "main_purpose_of_visit": "Tourism",
            "travel_budget": 2000.0,
            "duration_of_visit": 7,
            "preferred_attractions": "Nature",
            "special_activities_interested": "Hiking, local cuisine tasting",
            "number_of_people_travelling": 2,
            "transportation_preferences": "Car rental",
            "accommodation_preferences": "Hotel",
            "interested_places": ["Grand Canyon", "Yellowstone National Park"],
            "weather_preference": "Warm",
            "month_of_visit": ["July", "August"],
        }
    }
