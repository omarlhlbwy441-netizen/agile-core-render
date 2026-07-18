from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/project/{project_id}/overview")
def get_project_overview(project_id: str, db: Session = Depends(get_db)):
    project = ProjectService.get_by_id(db, project_id)
    tasks = TaskService.get_by_project(db, project_id)

    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status.value == "done"])
    in_progress = len([t for t in tasks if t.status.value == "in_progress"])
    total_points = sum(t.story_points for t in tasks)
    completed_points = sum(t.story_points for t in tasks if t.status.value == "done")

    return {
        "project_id": project_id,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress": in_progress,
        "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        "total_story_points": total_points,
        "completed_story_points": completed_points,
        "velocity": completed_points,
    }

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    from sqlalchemy import func
    from app.models.project import Project
    from app.models.task import Task

    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "done").count()

    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "active_projects": db.query(Project).filter(Project.status == "active").count(),
    }
