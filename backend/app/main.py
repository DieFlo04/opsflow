from fastapi import FastAPI

app = FastAPI(
    title="OpsFlow API",
    description="IT Operations & Automation Platform",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "OpsFlow API is running"
    }