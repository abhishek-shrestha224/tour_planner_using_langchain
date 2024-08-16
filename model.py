from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Data(BaseModel):
  id: Optional[UUID] = None
  title: str
  body: Optional[str] = None
  is_compeleted: Optional[bool] = False
