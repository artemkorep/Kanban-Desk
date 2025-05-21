from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.crud import get_task_by_id, get_task_logs_by_id
from src.schemas.logs import LogInfo, LogsInfo

router = APIRouter()


@router.get("/{id}", summary="Get logs task by id")
async def get_logs_task(
    task_id: int, db: AsyncSession = Depends(get_async_db)
) -> LogsInfo:
    task = await get_task_by_id(task_id=task_id, db=db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    logs = await get_task_logs_by_id(task_id=task_id, db=db)
    logs_list = [
        LogInfo(message=log.message, user_id=log.user_id, date=log.created_at)
        for log in logs
    ]

    return LogsInfo(logs=logs_list)
