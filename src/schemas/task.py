from datetime import datetime, timezone
from pydantic import BaseModel, field_validator


class TaskBase(BaseModel):
    title: str
    description: str = None
    due_date: datetime = None
    column_id: int
    order: int

    @field_validator("due_date")
    def validate_due_date(cls, value):
        if value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value


class TaskInfo(BaseModel):
    id: int
    title: str
    description: str = None
    due_date: datetime = None
    column_id: int
    author_id: int
    order: int
    created_at: datetime
    updated_at: datetime


class TaskUpdateInfo(BaseModel):
    title: str = None
    description: str = None
    due_date: datetime = None

    @field_validator("due_date")
    def validate_due_date(cls, value):
        if value.tzinfo is not None and value.tzinfo.utcoffset(value) is not None:
            return value.astimezone(timezone.utc).replace(tzinfo=None)
        return value


class TaskUpdateOrderInfo(BaseModel):
    order: int = None
    column_id: int = None
