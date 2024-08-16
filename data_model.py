from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class DataModel(BaseModel):
  id: Optional[UUID] = None
  first_name: str
  last_name: str
  country_of_origin: str
  occupation: str
  main_purpose_of_visit: str
  travel_budget: float
  duration_of_visit: int
  food_preferences: str
  preferred_attractions: str
  number_of_people_travelling: int
  special_activities_interested: Optional[str] = None
  transportation_preferences: Optional[str] = None
  accommodation_preferences: Optional[str] = None
  interested_places: Optional[List[str]] = None
  weather_preference: Optional[str] = None
  from_month: Optional[str] = None
  from_to: Optional[str] = None
