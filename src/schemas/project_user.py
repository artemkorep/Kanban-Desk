from typing import Sequence
from pydantic import BaseModel


class ProjectUserInfo(BaseModel):
    project_id: int
    user_id: int


class UserIdsResponse(BaseModel):
    user_ids: Sequence[int]
