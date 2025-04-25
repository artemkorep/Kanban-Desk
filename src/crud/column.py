from typing import Sequence

from fastapi import Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.models import Column
from src.schemas import ColumnBase, UpdateColumnInfo


# adsdsadfads
async def create_column_crud(
    column: ColumnBase,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> Column:

    db_column = Column(
        name=column.name, project_id=column.project_id, order=column.order
    )
    db.add(db_column)
    await db.commit()
    await db.refresh(db_column)

    return db_column


async def get_project_all_columns(
    project_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> Sequence[Column]:
    result = await db.execute(select(Column).filter(Column.project_id == project_id))
    columns = result.scalars().all()

    if not columns:
        return []

    return columns


async def get_column_by_id_crud(
    column_id: int, db: AsyncSession = Depends(get_async_db)
) -> Column:
    result = await db.execute(select(Column).where(Column.id == column_id))
    project = result.scalars().first()

    return project


async def update_column_by_id(
    column_id: int,
    updated_column: UpdateColumnInfo,
    db: AsyncSession = Depends(get_async_db),
) -> Column:
    column = await get_column_by_id_crud(column_id=column_id, db=db)

    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")

    if updated_column.name:
        column.name = updated_column.name
    if updated_column.order:
        column.order = updated_column.order

    await db.commit()
    await db.refresh(column)
    return column


async def delete_column_by_id(
    column_id: int, db: AsyncSession = Depends(get_async_db)
) -> bool:
    column = await get_column_by_id_crud(column_id=column_id, db=db)
    if not column:
        raise HTTPException(
            status_code=404,
            detail=f"Column with id {column_id} not found",
        )
    await db.delete(column)
    await db.commit()
    return True
