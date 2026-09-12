from fastapi import FastAPI

from backend.app.api.users import router as users_router
from backend.app.api.incidents import router as incidents_router


app = FastAPI(
    title="OpsFlow API",
    description="IT Operations & Automation Platform",
    version="1.0.0"
)


app.include_router(users_router, prefix="/api")
app.include_router(incidents_router, prefix="/api")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "OpsFlow API is running"
    }