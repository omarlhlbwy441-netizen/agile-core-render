from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.task import TaskPriority, TaskStatus

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.BACKLOG
    story_points: int = 0

class TaskCreate(TaskBase):
    project_id: str
    sprint_id: Optional[str] = None
    assignee_id: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    story_points: Optional[int] = None
    assignee_id: Optional[str] = None
    sprint_id: Optional[str] = None

class TaskResponse(TaskBase):
    id: str
    project_id: str
    sprint_id: Optional[str] = None
    assignee_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    assignee_name: Optional[str] = None

    class Config:
        from_attributes = True
