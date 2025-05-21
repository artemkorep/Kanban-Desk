from typing import Sequence

from fastapi.params import Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.models import TaskLog


async def get_task_logs_by_id(
    task_id: int, db: AsyncSession = Depends(get_async_db)
) -> Sequence[TaskLog]:
    result = await db.execute(select(TaskLog).filter(TaskLog.task_id == task_id))
    projects = result.scalars().all()

    if not projects:
        return []

    return projects
