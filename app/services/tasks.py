from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session, user: User, skip: int = 0, limit: int = 50) -> list[Task]:
    return db.query(Task).filter(Task.owner_id == user.id).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int, user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def create_task(db: Session, data: TaskCreate, user: User) -> Task:
    task = Task(**data.model_dump(), owner_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, data: TaskUpdate, user: User) -> Task:
    task = get_task(db, task_id, user)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user: User) -> None:
    task = get_task(db, task_id, user)
    db.delete(task)
    db.commit()
