from fastapi import APIRouter
from src.routers.auth import router as auth
from src.routers.project import router as project


router = APIRouter(prefix="/api")
router.include_router(auth, prefix="/auth", tags=["Authorization"])
router.include_router(project, prefix="/project", tags=["Project"])
