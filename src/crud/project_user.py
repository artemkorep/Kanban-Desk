from typing import Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import delete, and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.models import ProjectUser


async def add_user_to_project_by_id(
    user_id: int,
    project_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> ProjectUser:
    db_project = ProjectUser(project_id=project_id, user_id=user_id)

    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)

    return db_project


async def get_user_by_project(
    project_id: int, user_id: int, db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(
        select(ProjectUser).filter_by(project_id=project_id, user_id=user_id)
    )
    return result.scalar_one_or_none()


async def get_all_project_users(
    project_id: int, db: AsyncSession = Depends(get_async_db)
) -> Sequence[int]:
    result = await db.execute(
        select(ProjectUser.user_id).filter(ProjectUser.project_id == project_id)
    )
    user_ids = result.scalars().all()
    return user_ids


async def remove_user_from_project(
    project_id: int, user_id: int, db: AsyncSession = Depends(get_async_db)
) -> None:
    result = await get_user_by_project(project_id=project_id, user_id=user_id, db=db)
    if not result:
        raise HTTPException(status_code=404, detail=f"User not found for this project")
    await db.delete(result)
    await db.commit()
