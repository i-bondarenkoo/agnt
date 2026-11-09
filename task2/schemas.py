from typing import TypedDict
from enum import Enum

from pydantic import BaseModel, Field


class TypeMessage(str, Enum):
    """Варианты типов сообщений, которые может прислать пользователь."""

    # жалоба
    complaint = "complaint"
    # вопрос
    question = "question"
    # благодарность
    gratitude = "gratitude"


class StateAll(TypedDict):
    """Общее состояние, передается на вход узлам."""

    user_message: str
    type_message: TypeMessage
    finally_response: str


class StateAfterReadPrompt(BaseModel):
    """Модель для хранения данных из сообщения пользователя"""

    type_message: TypeMessage = Field(
        description=f"Значение атрибута должно быть объектом класса {TypeMessage}"
    )


class ResponseForQuestion(BaseModel):
    """Ответ пользователя на сообщение с вопросом"""

    finally_response: str = Field(
        description="Ответ пользователю, начни с фразы 'Хороший вопрос, давай обсудим' и предложи решение проблемы",
    )


class ResponseForComplaint(BaseModel):
    """Ответ пользователя на сообщение с вопросом"""

    finally_response: str = Field(
        description="Ответ пользователю, начни с фразы 'Я тебя прекрасно понимаю, давай вместе разберемся с твоей проблемой' и предложи решение проблемы",
    )


class ResponseForGratitude(BaseModel):
    """Ответ пользователя на сообщение с вопросом"""

    finally_response: str = Field(
        description="Ответ пользователю, начни с фразы 'Спасибо, я рад что смог помочь тебе' и предложи решение проблемы",
    )
