import chromadb
from langgraph.graph import StateGraph, START, END
from task3.knowledge import KNOWLEDGE_BASE
from task3.schemas import (
    DocumentSearchState,
    DataBaseResponse,
    GenerateAnswerOutput,
)
from llm_model import llm_model

# база в оперативной памяти (клиент chroma)
client = chromadb.Client()
# таблица внутри базы с именем knowledge
# в коллекциях хранятся эмбеддинги(Вектора), документы и другие метаданные
collection = client.create_collection("knowledge")

# формат хранения данных
# в примере список строк
# бд сама обрабатывает каждый текст через модель embeddnigs
# сохраняет текст и его вектор(числовое значение)
# так же добавляем ид в виде строки
collection.add(
    documents=KNOWLEDGE_BASE, ids=[str(i) for i in range(len(KNOWLEDGE_BASE))]
)


def retrieve(state: DocumentSearchState):
    result = collection.query(
        query_texts=[state.user_text],
        n_results=state.documents_count,
    )
    documents = []
    for i in range(len(result["documents"][0])):
        documents.append(
            DataBaseResponse(
                ids=int(result["ids"][0][i]),
                document=result["documents"][0][i],
            ),
        )
    return {"documents": documents}


def generate_response(state: DocumentSearchState):
    context = "\n\n".join(doc.document for doc in state.documents)
    prompt = f"Вопрос пользователя: {state.user_text}\n\nКонтекст:\n{context}\n\nОтветь на вопрос, используя только этот контекст."
    structured_output_model = llm_model.with_structured_output(GenerateAnswerOutput)
    result = structured_output_model.invoke(prompt)
    return {"answer": result.answer}


graph = (
    StateGraph(DocumentSearchState)
    .add_node("retrieve", retrieve)
    .add_node("generate_response", generate_response)
    .add_edge(START, "retrieve")
    .add_edge("retrieve", "generate_response")
    .add_edge("generate_response", END)
    .compile()
)

if __name__ == "__main__":
    result = graph.invoke(
        {
            "user_text": "Что ты знаешь о FastAPI",
            "documents": [],
            "documents_count": 15,
            "answer": "",
        }
    )
    print(result["answer"])

# пример ответа с базы
# {
#     "ids": [["0", "4"]],
#     "embeddings": None,
#     "documents": [
#         [
#             "CRUD — это аббревиатура от Create, Read, Update, Delete. Это четыре базовые операции для работы с данными: создание записи, чтение записи, обновление записи и удаление записи. В FastAPI они обычно реализуются как четыре разных эндпоинта с методами POST, GET, PUT/PATCH и DELETE.",
#             "Pydantic используется в FastAPI для валидации входящих и исходящих данных. Схема описывается как класс с полями и их типами, и FastAPI автоматически проверяет запрос на соответствие этой схеме, а также формирует документацию API на основе этих схем.",
#         ]
#     ],
#     "uris": None,
#     "included": ["metadatas", "documents", "distances"],
#     "data": None,
#     "metadatas": [[None, None]],
#     "distances": [[1.057692527770996, 1.204237937927246]],
# }
