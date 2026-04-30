from typing import List
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# Хранилище в памяти
db = []
next_id = 1


@strawberry.type
class Like:
    id: int
    target: str


@strawberry.type
class Query:
    @strawberry.field
    def likes(self) -> List[Like]:
        return db

    @strawberry.field
    def like(self, id: int) -> Like | None:
        for item in db:
            if item.id == id:
                return item
        return None


@strawberry.type
class Mutation:
    @strawberry.mutation    
    def createLike(self, target: str) -> Like:
        global next_id

        item = Like(id=next_id, target=target)
        db.append(item)
        next_id += 1

        return item


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
