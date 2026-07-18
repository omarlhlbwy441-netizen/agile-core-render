from sqlalchemy.orm import Session
from app.models.sprint import Sprint
from app.schemas.sprint import SprintCreate, SprintUpdate
from uuid import uuid4

class SprintService:
    @staticmethod
    def get_by_id(db: Session, sprint_id: str):
        return db.query(Sprint).filter(Sprint.id == sprint_id).first()

    @staticmethod
    def get_by_project(db: Session, project_id: str):
        return db.query(Sprint).filter(Sprint.project_id == project_id).all()

    @staticmethod
    def create(db: Session, sprint_data: SprintCreate):
        db_sprint = Sprint(
            id=str(uuid4()),
            name=sprint_data.name,
            goal=sprint_data.goal,
            status=sprint_data.status,
            start_date=sprint_data.start_date,
            end_date=sprint_data.end_date,
            velocity=sprint_data.velocity,
            project_id=sprint_data.project_id
        )
        db.add(db_sprint)
        db.commit()
        db.refresh(db_sprint)
        return db_sprint

    @staticmethod
    def update(db: Session, sprint: Sprint, sprint_data: SprintUpdate):
        for field, value in sprint_data.dict(exclude_unset=True).items():
            setattr(sprint, field, value)
        db.commit()
        db.refresh(sprint)
        return sprint

    @staticmethod
    def delete(db: Session, sprint: Sprint):
        db.delete(sprint)
        db.commit()
