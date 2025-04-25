from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.database import get_async_db
from src.core.dependencies import get_current_user
from src.crud import (
    add_user_to_project_by_id,
    get_project_by_id_crud,
    get_user_by_id,
    get_all_project_users,
    get_user_by_project,
    remove_user_from_project,
)
from src.models import User
from src.schemas import ProjectUserInfo, UserIdsResponse

router = APIRouter()


@router.post("", summary="Add user to project")
async def add_user_to_project(
    project_id: int,
    participant_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
) -> ProjectUserInfo:
    project = await get_project_by_id_crud(project_id=project_id, db=db)
    participant = await get_user_by_id(user_id=user.id, db=db)
    project_user = await get_user_by_project(
        user_id=participant_id, project_id=project_id, db=db
    )
    if project_user:
        raise HTTPException(status_code=409, detail="User already added to project")
    if not project:
        raise HTTPException(status_code=404, detail=f"Project not found")
    if not participant:
        raise HTTPException(
            status_code=404, detail="Participant with sent id not found"
        )
    if project.author_id != user.id:
        raise HTTPException(
            status_code=403, detail=f"You are not the author of the project"
        )

    result = await add_user_to_project_by_id(
        user_id=participant_id, project_id=project_id, db=db
    )

    return ProjectUserInfo(
        project_id=result.project_id,
        user_id=result.user_id,
    )


@router.get("", summary="Get users list")
async def get_user_list(
    project_id: int, db: AsyncSession = Depends(get_async_db)
) -> UserIdsResponse:
    project = await get_project_by_id_crud(project_id=project_id, db=db)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project not found")

    user_ids = await get_all_project_users(project_id=project_id, db=db)

    return UserIdsResponse(user_ids=user_ids)


@router.delete("/{user_id}", summary="Delete user from project")
async def delete_user_from_project(
    participant_id: int,
    project_id,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
) -> bool:
    project = await get_project_by_id_crud(project_id=project_id, db=db)

    if not project:
        raise HTTPException(status_code=404, detail=f"Project not found")
    if user.id != project.author_id:
        raise HTTPException(
            status_code=403, detail=f"You are not the author of the project"
        )

    await remove_user_from_project(project_id=project_id, user_id=user.id, db=db)
    return True
