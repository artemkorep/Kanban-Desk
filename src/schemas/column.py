from datetime import datetime
from typing import List

from pydantic import BaseModel


class ColumnBase(BaseModel):
    name: str
    project_id: int
    order: int


class UpdateColumnInfo(BaseModel):
    name: str = None
    order: int = None


class ColumnList(BaseModel):
    columns: List[ColumnBase]


class ColumnInfo(BaseModel):
    id: int
    name: str
    project_id: int
    order: int
    created_at: datetime
    updated_at: datetime
