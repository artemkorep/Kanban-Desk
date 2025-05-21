from datetime import datetime
from typing import List

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: str = None


class ProjectList(BaseModel):
    projects: List[ProjectBase]


class ProjectUpdateInfo(BaseModel):
    name: str = None
    description: str = None


class ProjectInfo(BaseModel):
    id: int
    name: str
    description: str = None
    author_id: int
    created_at: datetime
    updated_at: datetime


class ProjectFilters(BaseModel):
    author_id: int = None
