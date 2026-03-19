from fastapi import APIRouter

from app.api.comments import router as comments_router
from app.api.general import router as general_router

router = APIRouter(prefix="/api", tags=["User Activity"])
router.include_router(comments_router)
router.include_router(general_router)
