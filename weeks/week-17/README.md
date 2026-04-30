# tasks-s22

Сервис управления задачами. Группа 331, студент s22.

## Что это?

REST API для работы со списком задач (CRUD). Поле `due` — срок выполнения.

## Архитектура

- **gateway** — REST-фасад на FastAPI, порт `8236`
- **tasks-svc** — gRPC-сервис с SQLite, порт `50051` (внутренний)

Подробнее: [ARCHITECTURE.md](ARCHITECTURE.md)

## Как запустить

```bash
git clone <repo>
cd tasks-s22
docker compose up --build
```

Готово. API доступно на `http://localhost:8236`.

## Примеры запросов

```bash
# Создать задачу
curl -X POST http://localhost:8236/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Сдать проект", "due": "2025-06-01"}'

# Список задач
curl http://localhost:8236/api/tasks

# Обновить задачу
curl -X PUT http://localhost:8236/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Сдать проект", "due": "2025-06-01", "done": true}'

# Удалить задачу
curl -X DELETE http://localhost:8236/api/tasks/1
```

## Swagger UI

`http://localhost:8236/docs`

## Структура проекта

```
tasks-s22/
├── proto/
│   └── tasks.proto          # gRPC-контракт
├── tasks-svc/
│   ├── main.py              # gRPC-сервер
│   ├── tasks_pb2.py         # сгенерировано из proto
│   ├── tasks_pb2_grpc.py    # сгенерировано из proto
│   ├── requirements.txt
│   └── Dockerfile
├── gateway/
│   ├── main.py              # FastAPI REST → gRPC
│   ├── tasks_pb2.py         # сгенерировано из proto
│   ├── tasks_pb2_grpc.py    # сгенерировано из proto
│   ├── requirements.txt
│   └── Dockerfile
├── k8s/
│   ├── tasks-svc.yaml
│   └── gateway.yaml
├── .github/workflows/
│   └── ci.yml
├── docker-compose.yml
├── ARCHITECTURE.md
└── README.md
```
