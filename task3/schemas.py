from pydantic import BaseModel, Field


class DataBaseResponse(BaseModel):
    """
    Подходящий текст по запросу юзера из базы.
    """

    ids: int = Field(description="Идентификатор строки в БД")
    document: str = Field(description="Текст из БД")


class DocumentSearchState(BaseModel):
    """
    Состояние запроса. Передается между узлами.
    """

    user_text: str = Field(description="Вопрос пользователя")
    documents: list[DataBaseResponse] = Field(description="Текст из БД")
    documents_count: int = Field(ge=1, description="Количество ответов на вопрос")
    answer: str = Field(default="", description="Финальный ответ пользователя")


class GenerateAnswerOutput(BaseModel):
    """
    Схема ответа модели с текстом из БД.
    """

    answer: str = Field(description="Ответ пользователю на основе текста из БД")
