from typing import TypedDict
from pydantic import BaseModel, Field


# 1 день поездки
class DayPlan(TypedDict):
    # порядковый номер дня поездки - 1, 2
    day_number: int
    # общая тема дня
    theme: str
    # конкретные активности
    activities: list[str]


# Вся поездка
class TripState(TypedDict):
    # место, куда поедем
    destination: str
    # список дней поездки
    days_plan: list[DayPlan]
    # сколько дней уже заполнено активностями
    current_day_index: int
    # сколько дней длится поездка
    nums_day: int


class DayTheme(BaseModel):
    """Тема одного дня поездки."""

    day_number: int = Field(description="Порядковый номер дня поездки")
    theme: str = Field(description="Тема дня, например 'музеи и история'")


class GeneratePlanOutput(BaseModel):
    """План поездки: список тем по дням."""

    days: list[DayTheme] = Field(
        description="Список тем, по одной на каждый день поездки"
    )


class ListActivities(BaseModel):
    """Список активностей по дням"""

    actions: list[str]
