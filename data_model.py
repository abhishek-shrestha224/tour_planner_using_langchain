from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class DataModel(BaseModel):
  first_name: str
  last_name: str
  country_of_origin: str
  occupation: str
  main_purpose_of_visit: str
  travel_budget: float
  duration_of_visit: int
  food_preferences: Optional[List[str]]
  preferred_attractions: Optional[List[str]]
  number_of_people_travelling: int
  special_activities_interested: Optional[List[str]] = None
  transportation_preferences: Optional[str] = None
  accommodation_preferences: Optional[str] = None
  interested_places: Optional[List[str]] = None
  weather_preference: Optional[str] = None
  from_month: Optional[str] = None
  to_month: Optional[str] = None
