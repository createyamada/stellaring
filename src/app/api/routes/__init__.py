from fastapi import APIRouter
from app.api.routes.equationOfMotion import router as equationOfMotion_router
from app.api.routes.kepler_router import router as kepler_router
from app.api.routes.test_router import router as test_router

router = APIRouter()
router.include_router(equationOfMotion_router, prefix="/equationOfMotion", tags=["equationOfMotion"])
router.include_router(kepler_router, prefix="/kepler", tags=["kepler"])
router.include_router(test_router, prefix="/test", tags=["test"])
