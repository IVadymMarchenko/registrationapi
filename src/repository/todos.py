from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db
from src.entity.models import Todo
from src.schemas.todo import TodoSchema, TodoUpdate, TodoResponse


async def get_todos(limit: int, offset: int, db: AsyncSession):  # Получение всех задач
    smt = select(Todo).offset(offset).limit(limit)
    todos = await db.execute(smt)
    return todos.scalar().all()


async def get_todo(todo_id: int, db: AsyncSession):  # Получение одной задачи
    smt = select(Todo).filter_by(id=todo_id)
    todo = await db.execute(smt)
    return todo.scalar_one_or_none()


async def create_todo(body: TodoSchema, db: AsyncSession):  # Создание задачи
    todo = Todo(**body.model_dump(exclude_unset=True))
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(todo_id: int, body: TodoUpdate, db: AsyncSession):
    stmt = select(Todo).filter_by(id=todo_id)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()
    if todo:
        todo.title = body.title
        todo.descriotion = body.descriotion
        todo.completed = body.completed
        await db.commit()
        await db.refresh(todo)
    return todo


async def delete_todo(todo_id: int, db: AsyncSession):  # Удаление задачи
    smt = select(Todo).filter_by(id=todo_id)
    todo = await db.execute(smt)
    todo=todo.scalar_one_or_none()
    if todo:
        await db.delete(todo)
        await db.commit()
    return todo


