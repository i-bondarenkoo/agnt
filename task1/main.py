from langchain_gigachat import GigaChat
from langgraph.graph import END, StateGraph, START

from task1.schemas import GeneratePlanOutput, TripState, ListActivities
from llm_model import llm_model


def generate_plan(state: TripState):
    """
    Функция генерирует план по поездке, место и количество дней вводит пользователь.
    """
    prompt = f"Пользователь едет в {state['destination']} на {state['nums_day']}. Придумай тему для каждого дня поездки"
    model_with_structure = llm_model.with_structured_output(GeneratePlanOutput)
    result = model_with_structure.invoke(prompt)
    # print(result)
    days_plan = [
        {"day_number": day.day_number, "theme": day.theme, "activities": []}
        for day in result.days
    ]
    return {"days_plan": days_plan}


def fill_day(state: TripState):
    """Заполняет 1 день активностями - тот, на который указывает current_day_index"""
    index = state["current_day_index"]
    day = state["days_plan"][index]

    prompt = f"Для конкретной темы {day['theme']} составь план активностей"
    model_wtih_structute = llm_model.with_structured_output(ListActivities)
    result = model_wtih_structute.invoke(prompt)

    update_day = {**day, "activities": result.actions}
    new_days_plan = state["days_plan"].copy()
    new_days_plan[index] = update_day
    return {"days_plan": new_days_plan, "current_day_index": index + 1}


def end_or_continue(state: TripState):
    if state["current_day_index"] < len(state["days_plan"]):
        return "fill_day"
    return END


# state = {
#     "days_plan": [
#         {"day_number": 1, "theme": "музеи и история", "activities": []},
#         {"day_number": 2, "theme": "кулинария и традиции", "activities": []},
#         {
#             "day_number": 3,
#             "theme": "современная Казань и развлечения",
#             "activities": [],
#         },
#     ],
#     "current_day_index": 0,
# }
graph = (
    StateGraph(TripState)
    .add_node("generate_plan", generate_plan)
    .add_node("fill_day", fill_day)
    .add_edge(START, "generate_plan")
    .add_edge("generate_plan", "fill_day")
    .add_conditional_edges("fill_day", end_or_continue)
    .compile()
)
if __name__ == "__main__":
    result = graph.invoke(
        {
            "destination": "Красноярск",
            "days_plan": [],
            "current_day_index": 0,
            "nums_day": 4,
        }
    )
    print(result)
