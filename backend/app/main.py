from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
# from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from app.api.v2 import twitter_router

# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_STR}/openapi.json",
)

# app.add_middleware(
#     SQLAlchemyMiddleware,
#     db_url=settings.ASYNC_DATABASE_URI,
#     engine_args={
#         "echo": False,
#         "pool_pre_ping": True,
#         "pool_size": settings.POOL_SIZE,
#         "max_overflow": 64,
#     },
# )

# Set all CORS origins enabled
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(twitter_router.router)
