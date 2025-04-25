from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.core.dependencies import get_current_user
from src.crud import (
    create_task_crud,
    get_task_by_id,
    update_task_by_id,
    update_task_order_or_column_crud,
    delete_task_by_id,
)
from src.models import User
from src.schemas import TaskBase, TaskInfo, TaskUpdateInfo, TaskUpdateOrderInfo

router = APIRouter()


@router.post("/create", summary="Create a new task")
async def create_task(
    task: TaskBase,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
) -> TaskInfo:
    task = await create_task_crud(task=task, author_id=user.id, db=db)
    return TaskInfo(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        column_id=task.column_id,
        author_id=task.author_id,
        order=task.order,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.get("/{id}", summary="Get a task info by id")
async def get_task(task_id: int, db: AsyncSession = Depends(get_async_db)) -> TaskInfo:
    task = await get_task_by_id(task_id=task_id, db=db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskInfo(
        id=task.id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        column_id=task.column_id,
        author_id=task.author_id,
        order=task.order,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.put("/{id}", summary="Update a task info")
async def update_task_info(
    task_id: int,
    updated_info: TaskUpdateInfo,
    db: AsyncSession = Depends(get_async_db),
    user: User = Depends(get_current_user),
) -> TaskInfo:
    task = await get_task_by_id(task_id=task_id, db=db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = await update_task_by_id(
        user_id=task.author_id, task_id=task.id, updated_info=updated_info, db=db
    )

    return TaskInfo(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        due_date=updated_task.due_date,
        column_id=updated_task.column_id,
        author_id=updated_task.author_id,
        order=updated_task.order,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at,
    )


@router.patch("/{id}/move", summary="Update a task order, column_id")
async def update_task_order_or_column(
    task_id: int,
    updated_info: TaskUpdateOrderInfo,
    db: AsyncSession = Depends(get_async_db),
    user: User = Depends(get_current_user),
) -> TaskInfo:
    task = await get_task_by_id(task_id=task_id, db=db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = await update_task_order_or_column_crud(
        user_id=task.author_id, task_id=task.id, updated_info=updated_info, db=db
    )

    return TaskInfo(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        due_date=updated_task.due_date,
        column_id=updated_task.column_id,
        author_id=updated_task.author_id,
        order=updated_task.order,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at,
    )


@router.delete("/{id}", summary="Delete a task")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_db),
    user: User = Depends(get_current_user),
) -> bool:
    await delete_task_by_id(task_id=task_id, user_id=user.id, db=db)
    return True
