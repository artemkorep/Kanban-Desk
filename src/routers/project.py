from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.core.dependencies import get_current_user
from src.crud.project import (
    create_project_crud,
    get_project_by_id_crud,
    delete_project_by_id,
    update_project_by_id,
    get_all_projects_by_id,
)
from src.models import User
from src.schemas.project import ProjectBase, ProjectInfo, ProjectUpdateInfo, ProjectList

router = APIRouter()


@router.post("/create", summary="Create new project")
async def create_project(
    project: ProjectBase,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
) -> ProjectInfo:
    project = await create_project_crud(project=project, author_id=user.id, db=db)
    return ProjectInfo(
        id=project.id,
        name=project.name,
        description=project.description,
        author_id=project.author_id,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


@router.get("/{id}", summary="Get project by id")
async def get_project_by_id(
    project_id: int, db: AsyncSession = Depends(get_async_db)
) -> ProjectInfo:
    project = await get_project_by_id_crud(project_id=project_id, db=db)
    return ProjectInfo(
        id=project.id,
        name=project.name,
        description=project.description,
        author_id=project.author_id,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


@router.delete("/{id}", summary="Delete project by id")
async def delete_project(
    project_id: int, db: AsyncSession = Depends(get_async_db)
) -> bool:
    project = await delete_project_by_id(project_id=project_id, db=db)
    return project


@router.put("/{id}", summary="Update project by id")
async def update_project(
    project_id: int,
    updated_info: ProjectUpdateInfo,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
) -> ProjectInfo:
    updated_project = await update_project_by_id(
        user_id=user.id, project_id=project_id, updated_info=updated_info, db=db
    )
    return ProjectInfo(
        id=updated_project.id,
        name=updated_project.name,
        description=updated_project.description,
        author_id=updated_project.author_id,
        created_at=updated_project.created_at,
        updated_at=updated_project.updated_at,
    )


@router.get("/", summary="Get all user projects")
async def get_all_projects_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    projects = await get_all_projects_by_id(user_id=user_id, db=db)
    project_list = [
        ProjectBase(name=project.name, description=project.description)
        for project in projects
    ]

    return ProjectList(projects=project_list)
