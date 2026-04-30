import requests

PROJECT_CODE = "orders-s22"

# Реализация клиента
def build_payload(query: str, variables: dict = None) -> dict:
    return {
        "query": query,
        "variables": variables or {}
    }

def call_graphql(url: str, query: str, variables: dict = None):
    payload = build_payload(query, variables)
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "errors" in result:
            print(f"Ошибки GraphQL: {result['errors']}")
            
        return result.get("data")
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return None


URL = "http://127.0.0.1:8000/graphql"

# Мутация: создаем лайк, используя PROJECT_CODE как цель (target)
create_mutation = """
mutation($target: String!) {
  createLike(target: $target) {
    id
    target
  }
}
"""

print(f"Создаем лайк для проекта: {PROJECT_CODE}")
created_data = call_graphql(URL, create_mutation, {"target": PROJECT_CODE})
print("Ответ сервера:", created_data)

# Запрос: получаем список всех лайков
list_query = """
query {
  likes {
    id
    target
  }
}
"""

print("\nТекущие лайки в базе:")
all_likes = call_graphql(URL, list_query)
print(all_likes)

# Запрос конкретного лайка по ID
get_one_query = """
query($id: Int!) {
  like(id: $id) {
    id
    target
  }
}
"""

print("\nЗапрашиваем лайк с ID=1:")
single_like = call_graphql(URL, get_one_query, {"id": 1})
print(single_like)
