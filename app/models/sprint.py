from sqlalchemy import Column, String, DateTime, Date, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class SprintStatus(str, enum.Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"

class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    goal = Column(String, nullable=True)
    status = Column(Enum(SprintStatus), default=SprintStatus.PLANNED)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    velocity = Column(Integer, default=0)
    project_id = Column(String, ForeignKey("projects.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="sprints")
    tasks = relationship("Task", back_populates="sprint")
