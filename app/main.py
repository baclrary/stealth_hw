from auth.auth import auth_backend, current_active_user, fastapi_users
from auth.schemas import UserCreate, UserRead
from fastapi import Depends, FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from products.routers import router as products_router
from redis import asyncio as aioredis
from tasks.tasks import send_report

from app.auth.models import User

app = FastAPI(title="Stealth startup homework")


@app.get("/")
def message_to_Borys():
    return {"Message to Borys": "Hello Borys, thank you for this opportunity!"}


@app.get("/long_task")
@cache(
    expire=3600  # I don't want user to spam with report generation,
    # so I would put 1h (3600s) limit here, it makes sense,
    # there's no need in big report generation (a year report) every hour and even more
    # !! Remove if you want to test celery queue and clear browser's cache.
)
async def long_task(user: User = Depends(current_active_user)):
    send_report.delay(user.email)
    return {
        "status": f"Started processing a report for {user.email}. "
        "It may take some time. You'll be notified upon completion."
    }


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(products_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
