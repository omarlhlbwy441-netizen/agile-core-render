from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.services.sprint_service import SprintService
from app.schemas.sprint import SprintCreate, SprintUpdate, SprintResponse

router = APIRouter(prefix="/sprints", tags=["Sprints"])

@router.get("/project/{project_id}", response_model=List[SprintResponse])
def get_sprints_by_project(project_id: str, db: Session = Depends(get_db)):
    return SprintService.get_by_project(db, project_id)

@router.post("/", response_model=SprintResponse, status_code=status.HTTP_201_CREATED)
def create_sprint(sprint_data: SprintCreate, db: Session = Depends(get_db)):
    return SprintService.create(db, sprint_data)

@router.get("/{sprint_id}", response_model=SprintResponse)
def get_sprint(sprint_id: str, db: Session = Depends(get_db)):
    sprint = SprintService.get_by_id(db, sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint

@router.put("/{sprint_id}", response_model=SprintResponse)
def update_sprint(sprint_id: str, sprint_data: SprintUpdate, db: Session = Depends(get_db)):
    sprint = SprintService.get_by_id(db, sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return SprintService.update(db, sprint, sprint_data)

@router.delete("/{sprint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sprint(sprint_id: str, db: Session = Depends(get_db)):
    sprint = SprintService.get_by_id(db, sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    SprintService.delete(db, sprint)
    return {"message": "Sprint deleted successfully"}
