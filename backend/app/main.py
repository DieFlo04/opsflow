from fastapi import FastAPI

from backend.app.api.users import router as users_router
from backend.app.api.incidents import router as incidents_router
from backend.app.api.comment import router as comments_router
from backend.app.api.systems import router as systems_router
from backend.app.api.categories import router as categories_router
from backend.app.api.auth import router as auth_router

app = FastAPI(
    title="OpsFlow API",
    description="IT Operations & Automation Platform",
    version="1.0.0"
)


app.include_router(users_router, prefix="/api")
app.include_router(incidents_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(systems_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "OpsFlow API is running"
    }