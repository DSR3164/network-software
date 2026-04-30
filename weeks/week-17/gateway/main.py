import os
import logging
import grpc
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import tasks_pb2
import tasks_pb2_grpc

logging.basicConfig(level=logging.INFO, format="%(asctime)s [gateway] %(message)s")
log = logging.getLogger(__name__)

TASKS_SVC_ADDR = os.getenv("TASKS_SVC_ADDR", "tasks-svc:50051")

app = FastAPI(title="Tasks Gateway", version="1.0.0")


def get_stub():
    channel = grpc.insecure_channel(TASKS_SVC_ADDR)
    return tasks_pb2_grpc.TasksServiceStub(channel)


def task_to_dict(task) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "due": task.due,
        "done": task.done,
    }


# ---------- Schemas ----------

class TaskCreate(BaseModel):
    title: str
    due: str = ""


class TaskUpdate(BaseModel):
    title: str
    due: str = ""
    done: bool = False


# ---------- Routes ----------

@app.get("/api/tasks")
def list_tasks():
    log.info("GET /api/tasks")
    stub = get_stub()
    resp = stub.ListTasks(tasks_pb2.ListTasksRequest())
    return [task_to_dict(t) for t in resp.tasks]


@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    log.info("GET /api/tasks/%s", task_id)
    stub = get_stub()
    try:
        resp = stub.GetTask(tasks_pb2.GetTaskRequest(id=task_id))
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Task not found")
        raise HTTPException(status_code=500, detail=str(e))
    return task_to_dict(resp.task)


@app.post("/api/tasks", status_code=201)
def create_task(body: TaskCreate):
    log.info("POST /api/tasks title=%s", body.title)
    stub = get_stub()
    resp = stub.CreateTask(tasks_pb2.CreateTaskRequest(title=body.title, due=body.due))
    return task_to_dict(resp.task)


@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate):
    log.info("PUT /api/tasks/%s", task_id)
    stub = get_stub()
    try:
        resp = stub.UpdateTask(tasks_pb2.UpdateTaskRequest(
            id=task_id,
            title=body.title,
            due=body.due,
            done=body.done,
        ))
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Task not found")
        raise HTTPException(status_code=500, detail=str(e))
    return task_to_dict(resp.task)


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    log.info("DELETE /api/tasks/%s", task_id)
    stub = get_stub()
    stub.DeleteTask(tasks_pb2.DeleteTaskRequest(id=task_id))
    return None


@app.get("/health")
def health():
    return {"status": "ok"}
