from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.core.dependencies import get_current_user
from src.crud import get_project_by_id_crud
from src.crud.column import (
    create_column_crud,
    get_project_all_columns,
    get_column_by_id_crud,
    update_column_by_id,
    delete_column_by_id,
)
from src.models import User
from src.schemas import ColumnBase, ColumnInfo, ColumnList, UpdateColumnInfo
from src.schemas.project import ProjectBase, ProjectInfo, ProjectUpdateInfo, ProjectList

router = APIRouter()


@router.post("/create", summary="Create new column for project")
async def create_column(
    column: ColumnBase,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
) -> ColumnInfo:
    project = await get_project_by_id_crud(project_id=column.project_id, db=db)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    column = await create_column_crud(column=column, db=db, user_id=user.id)
    return ColumnInfo(
        id=column.id,
        name=column.name,
        project_id=column.project_id,
        order=column.order,
        created_at=column.created_at,
        updated_at=column.updated_at,
    )


@router.get("/list", summary="List all columns")
async def list_columns(project_id: int, db: AsyncSession = Depends(get_async_db)):
    project = await get_project_by_id_crud(project_id=project_id, db=db)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    columns = await get_project_all_columns(project_id=project_id, db=db)
    columns_list = [
        ColumnBase(name=column.name, project_id=project_id, order=column.order)
        for column in columns
    ]

    return ColumnList(columns=columns_list)


@router.get("/{column_id}", summary="Get column by id")
async def get_column_by_id(column_id: int, db: AsyncSession = Depends(get_async_db)):
    column = await get_column_by_id_crud(column_id=column_id, db=db)

    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")

    return column


@router.put("/update", summary="Update column")
async def update_column(
    column_id: int,
    updated_info: UpdateColumnInfo,
    db: AsyncSession = Depends(get_async_db),
    user: User = Depends(get_current_user),
):
    updated_column = await update_column_by_id(
        column_id=column_id, updated_column=updated_info, db=db
    )

    return updated_column


@router.delete("/delete", summary="Delete column")
async def delete_column(column_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await delete_column_by_id(column_id=column_id, db=db)

    return result
