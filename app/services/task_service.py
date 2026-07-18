from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from uuid import uuid4

class TaskService:
    @staticmethod
    def get_by_id(db: Session, task_id: str):
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def get_by_project(db: Session, project_id: str, skip: int = 0, limit: int = 100):
        return db.query(Task).filter(Task.project_id == project_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_sprint(db: Session, sprint_id: str):
        return db.query(Task).filter(Task.sprint_id == sprint_id).all()

    @staticmethod
    def get_by_assignee(db: Session, assignee_id: str):
        return db.query(Task).filter(Task.assignee_id == assignee_id).all()

    @staticmethod
    def create(db: Session, task_data: TaskCreate):
        db_task = Task(
            id=str(uuid4()),
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            status=task_data.status,
            story_points=task_data.story_points,
            project_id=task_data.project_id,
            sprint_id=task_data.sprint_id,
            assignee_id=task_data.assignee_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def update(db: Session, task: Task, task_data: TaskUpdate):
        for field, value in task_data.dict(exclude_unset=True).items():
            setattr(task, field, value)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete(db: Session, task: Task):
        db.delete(task)
        db.commit()

    @staticmethod
    def get_kanban_board(db: Session, project_id: str):
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        board = {
            "backlog": [],
            "todo": [],
            "in_progress": [],
            "review": [],
            "done": []
        }
        for task in tasks:
            board[task.status.value].append(task)
        return board
