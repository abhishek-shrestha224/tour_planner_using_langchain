from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class DataModel(BaseModel):
  id: Optional[UUID] = None
  first_name: str
  last_name: str
