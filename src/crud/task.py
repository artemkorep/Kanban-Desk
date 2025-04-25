from typing import Sequence, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.models import Task
from src.schemas import TaskBase, TaskUpdateInfo, TaskUpdateOrderInfo
from src.service.task import TaskLogService


async def create_task_crud(
    task: TaskBase,
    author_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> Task:
    db_task = Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        column_id=task.column_id,
        author_id=author_id,
        order=task.order,
    )

    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    await TaskLogService(db).log_creation(
        task_id=db_task.id, user_id=author_id, title=task.title
    )

    return db_task


async def get_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> Optional[Task]:
    result = await db.execute(select(Task).where(Task.id == task_id))
    project = result.scalars().first()

    return project


async def update_task_by_id(
    user_id: int,
    task_id: int,
    updated_info: TaskUpdateInfo,
    db: AsyncSession = Depends(get_async_db),
) -> Task:
    task = await get_task_by_id(task_id=task_id, db=db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    log_service = TaskLogService(db)
    if updated_info.title:
        old_title = task.title
        task.title = updated_info.title
        await log_service.log_title_change(
            task_id=task_id,
            user_id=user_id,
            old_title=old_title,
            new_title=updated_info.title,
        )
    if updated_info.description:
        old_description = task.description
        task.description = updated_info.description
        await log_service.log_description_change(
            task_id=task_id,
            user_id=user_id,
            old_description=old_description,
            new_description=updated_info.description,
        )
    if updated_info.due_date:
        old_due_date = task.due_date
        task.due_date = updated_info.due_date
        await log_service.log_change_due_date(
            task_id=task_id,
            user_id=user_id,
            old_due_date=old_due_date,
            new_due_date=task.due_date,
        )
    await db.commit()
    await db.refresh(task)

    return task


async def update_task_order_or_column_crud(
    user_id: int,
    task_id: int,
    updated_info: TaskUpdateOrderInfo,
    db: AsyncSession = Depends(get_async_db),
) -> Task:
    task = await get_task_by_id(task_id=task_id, db=db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    log_service = TaskLogService(db)
    if updated_info.order:
        old_order = task.order
        task.order = updated_info.order
        await log_service.log_order_change(
            task_id=task_id,
            user_id=user_id,
            old_order=old_order,
            new_order=updated_info.order,
        )
    if updated_info.column_id:
        old_column = task.column_id
        task.column_id = updated_info.column_id
        await log_service.log_column_change(
            task_id=task_id,
            user_id=user_id,
            old_column_id=old_column,
            new_column_id=updated_info.column_id,
        )
    await db.commit()
    await db.refresh(task)

    return task


async def delete_task_by_id(
    task_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> None:
    task = await get_task_by_id(task_id=task_id, db=db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()
