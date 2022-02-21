from fastapi import APIRouter

from .endpoints import users,movies,image

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(movies.router, prefix="/movies", tags=["movies"])
router.include_router(image.router, prefix="/images", tags=["images"])
