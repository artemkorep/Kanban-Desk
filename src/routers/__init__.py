from fastapi import APIRouter
from .auth import router as auth


router = APIRouter(prefix="/api")
router.include_router(auth, prefix="/auth", tags=["Authorization"])
