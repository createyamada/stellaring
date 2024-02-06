from fastapi import APIRouter
from app.api.routes.equationOfMotion import router as equationOfMotion_router


router = APIRouter()
router.include_router(equationOfMotion_router, prefix="/equationOfMotion", tags=["equationOfMotion"])