from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.database import Base, engine
from backend.routers import auth, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)

frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))


@app.get("/tasks-ui", include_in_schema=False)
def serve_tasks():
    return FileResponse(os.path.join(frontend_path, "tasks.html"))
