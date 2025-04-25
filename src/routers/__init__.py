from fastapi import APIRouter
from src.routers.auth import router as auth
from src.routers.project import router as project
from src.routers.column import router as column
from src.routers.task import router as task
from src.routers.logs import router as logs
from src.routers.project_user import router as project_user

router = APIRouter(prefix="/api")
router.include_router(auth, prefix="/auth", tags=["Authorization"])
router.include_router(project, prefix="/project", tags=["Project"])
router.include_router(column, prefix="/column", tags=["Column"])
router.include_router(task, prefix="/task", tags=["Task"])
router.include_router(logs, prefix="/logs", tags=["Logs"])
router.include_router(project_user, prefix="/project_user", tags=["Project User"])
