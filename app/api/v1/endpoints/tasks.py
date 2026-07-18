from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.db.base import get_db
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/project/{project_id}", response_model=List[TaskResponse])
def get_tasks_by_project(project_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return TaskService.get_by_project(db, project_id, skip, limit)

@router.get("/sprint/{sprint_id}", response_model=List[TaskResponse])
def get_tasks_by_sprint(sprint_id: str, db: Session = Depends(get_db)):
    return TaskService.get_by_sprint(db, sprint_id)

@router.get("/kanban/{project_id}")
def get_kanban_board(project_id: str, db: Session = Depends(get_db)):
    return TaskService.get_kanban_board(db, project_id)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    return TaskService.create(db, task_data)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = TaskService.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = TaskService.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskService.update(db, task, task_data)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = TaskService.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    TaskService.delete(db, task)
    return {"message": "Task deleted successfully"}
