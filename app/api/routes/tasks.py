from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.auth import get_current_user
from app.services.tasks import create_task, delete_task, get_task, get_tasks, update_task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskOut])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return get_tasks(db, user, skip=skip, limit=limit)


@router.post("/", response_model=TaskOut, status_code=201)
async def create(data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_task(db, data, user)


@router.get("/{task_id}", response_model=TaskOut)
async def get_one(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_task(db, task_id, user)


@router.patch("/{task_id}", response_model=TaskOut)
async def update(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return update_task(db, task_id, data, user)


@router.delete("/{task_id}", status_code=204)
async def delete(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    delete_task(db, task_id, user)
