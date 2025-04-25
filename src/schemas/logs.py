from datetime import datetime
from typing import List

from pydantic import BaseModel


class LogInfo(BaseModel):
    message: str
    user_id: int
    date: datetime


class LogsInfo(BaseModel):
    logs: List[LogInfo]
