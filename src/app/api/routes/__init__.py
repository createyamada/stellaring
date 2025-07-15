from fastapi import APIRouter
from app.api.routes.parabolicMotion import router as parabolicMotion_router
from app.api.routes.simpleHarmonizeMotion import router as simpleHarmonizeMotion_router
from app.api.routes.kepler_router import router as kepler_router
from app.api.routes.calc_satellite import router as satellite_router
# from app.api.routes.auth import router as auth


router = APIRouter()
router.include_router(parabolicMotion_router, prefix="/parabolicMotion", tags=["parabolicMotion"])
router.include_router(simpleHarmonizeMotion_router, prefix="/simpleHarmonizeMotion", tags=["simpleHarmonizeMotion"])
router.include_router(kepler_router, prefix="/kepler", tags=["kepler"])
router.include_router(satellite_router, prefix="/calc_satellite", tags=["calc_satellite"])
# router.include_router(auth, prefix="/auth", tags=["auth"])
