from fastapi import APIRouter

from src.auth.router import router as auth_router
from src.constants import RouterPrefix

api_router = APIRouter()

main_router = APIRouter(prefix=RouterPrefix.MAIN)

main_router.include_router(auth_router, prefix=RouterPrefix.AUTH, tags=["Auth"])


@api_router.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


api_router.include_router(main_router)
