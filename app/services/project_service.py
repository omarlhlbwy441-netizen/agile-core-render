from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from uuid import uuid4

class ProjectService:
    @staticmethod
    def get_by_id(db: Session, project_id: str):
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def get_by_owner(db: Session, owner_id: str, skip: int = 0, limit: int = 100):
        return db.query(Project).filter(Project.owner_id == owner_id).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, project_data: ProjectCreate, owner_id: str):
        db_project = Project(
            id=str(uuid4()),
            name=project_data.name,
            description=project_data.description,
            status=project_data.status,
            owner_id=owner_id
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def update(db: Session, project: Project, project_data: ProjectUpdate):
        for field, value in project_data.dict(exclude_unset=True).items():
            setattr(project, field, value)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete(db: Session, project: Project):
        db.delete(project)
        db.commit()
