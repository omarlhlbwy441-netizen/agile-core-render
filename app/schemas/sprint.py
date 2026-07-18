from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.sprint import SprintStatus

class SprintBase(BaseModel):
    name: str
    goal: Optional[str] = None
    status: SprintStatus = SprintStatus.PLANNED
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    velocity: int = 0

class SprintCreate(SprintBase):
    project_id: str

class SprintUpdate(BaseModel):
    name: Optional[str] = None
    goal: Optional[str] = None
    status: Optional[SprintStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    velocity: Optional[int] = None

class SprintResponse(SprintBase):
    id: str
    project_id: str
    created_at: datetime
    task_count: int = 0
    completed_points: int = 0

    class Config:
        from_attributes = True
