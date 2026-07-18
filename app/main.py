from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.middleware.cors import setup_cors
from app.db.base import engine, Base
from app.api.v1.endpoints import auth, users, projects, sprints, tasks, analytics
from app.api.v1.websocket import realtime
from fastapi import WebSocket

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

setup_cors(app)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(sprints.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")

@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    await realtime.websocket_endpoint(websocket)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/")
def root():
    return {
        "message": "Welcome to AGILE Core System",
        "version": settings.VERSION,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
