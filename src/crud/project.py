from typing import Sequence, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.models import Project
from src.schemas import ProjectBase, ProjectUpdateInfo


async def create_project_crud(
    project: ProjectBase,
    author_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> Project:
    db_project = Project(
        name=project.name, description=project.description, author_id=author_id
    )

    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def get_project_by_id_crud(
    project_id: int, db: AsyncSession = Depends(get_async_db)
) -> Optional[Project]:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalars().first()

    return project


async def delete_project_by_id(
    project_id: int, db: AsyncSession = Depends(get_async_db)
) -> bool:
    project = await get_project_by_id_crud(project_id=project_id, db=db)
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Project with id {project_id} not found",
        )
    await db.delete(project)
    await db.commit()
    return True


async def update_project_by_id(
    user_id: int,
    project_id: int,
    updated_info: ProjectUpdateInfo,
    db: AsyncSession = Depends(get_async_db),
) -> Project:
    project = await get_project_by_id_crud(project_id=project_id, db=db)
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Project with id {project_id} not found",
        )
    if user_id != project.author_id:
        raise HTTPException(
            status_code=403,
            detail=f"Project with id {project_id} does not have author id {user_id}",
        )

    if updated_info.name:
        project.name = updated_info.name
    if updated_info.description:
        project.description = updated_info.description

    await db.commit()
    await db.refresh(project)

    return project


async def get_all_projects_by_id(
    user_id: int, db: AsyncSession = Depends(get_async_db)
) -> Sequence[Project]:
    result = await db.execute(select(Project).filter(Project.author_id == user_id))
    projects = result.scalars().all()

    if not projects:
        return []

    return projects
