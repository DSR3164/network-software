import grpc
import sqlite3
import logging
from concurrent import futures

import tasks_pb2
import tasks_pb2_grpc

logging.basicConfig(level=logging.INFO, format="%(asctime)s [tasks-svc] %(message)s")
log = logging.getLogger(__name__)

DB_PATH = "/data/tasks.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due   TEXT NOT NULL DEFAULT '',
                done  INTEGER NOT NULL DEFAULT 0
            )
        """)
    log.info("DB initialized at %s", DB_PATH)


def row_to_task(row) -> tasks_pb2.Task:
    return tasks_pb2.Task(
        id=row["id"],
        title=row["title"],
        due=row["due"],
        done=bool(row["done"]),
    )


class TasksServicer(tasks_pb2_grpc.TasksServiceServicer):

    def ListTasks(self, request, context):
        log.info("ListTasks")
        with get_conn() as conn:
            rows = conn.execute("SELECT * FROM tasks").fetchall()
        return tasks_pb2.ListTasksResponse(tasks=[row_to_task(r) for r in rows])

    def GetTask(self, request, context):
        log.info("GetTask id=%s", request.id)
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id=?", (request.id,)).fetchone()
        if row is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Task not found")
            return tasks_pb2.TaskResponse()
        return tasks_pb2.TaskResponse(task=row_to_task(row))

    def CreateTask(self, request, context):
        log.info("CreateTask title=%s due=%s", request.title, request.due)
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO tasks (title, due) VALUES (?, ?)",
                (request.title, request.due),
            )
            row = conn.execute("SELECT * FROM tasks WHERE id=?", (cur.lastrowid,)).fetchone()
        return tasks_pb2.TaskResponse(task=row_to_task(row))

    def UpdateTask(self, request, context):
        log.info("UpdateTask id=%s", request.id)
        with get_conn() as conn:
            conn.execute(
                "UPDATE tasks SET title=?, due=?, done=? WHERE id=?",
                (request.title, request.due, int(request.done), request.id),
            )
            row = conn.execute("SELECT * FROM tasks WHERE id=?", (request.id,)).fetchone()
        if row is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Task not found")
            return tasks_pb2.TaskResponse()
        return tasks_pb2.TaskResponse(task=row_to_task(row))

    def DeleteTask(self, request, context):
        log.info("DeleteTask id=%s", request.id)
        with get_conn() as conn:
            conn.execute("DELETE FROM tasks WHERE id=?", (request.id,))
        return tasks_pb2.DeleteTaskResponse(ok=True)


def serve():
    init_db()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    tasks_pb2_grpc.add_TasksServiceServicer_to_server(TasksServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    log.info("gRPC server listening on :50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
