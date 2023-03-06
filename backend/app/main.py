from fastapi import FastAPI, Depends
from app.core.database import AsyncSessionManager
from app.core.config import settings

app = FastAPI()

# Set all CORS origins enabled
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup_event():
    await async_session_manager.async_engine.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await async_session_manager.async_engine.disconnect()

app.include_router(users.router)