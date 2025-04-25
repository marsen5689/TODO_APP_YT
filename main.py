from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
import requests as rq


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database initialized")
    yield
    # Close the database connection if needed


app = FastAPI(title="ToDo App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tasks/{tg_id}")
async def get_tasks(tg_id: int):
    user = await rq.add_iser(tg_id)
    return await rq.get_tasks(user.id)

@app.get("/api/tasks/{tg_id}")
async def get_tasks(tg_id: int):
    user = await rq.add_iser(tg_id)
    completed_tasks_count = await rq.get_completed_tasks(user.id)
    return {'completedTasks': completed_tasks_count}
