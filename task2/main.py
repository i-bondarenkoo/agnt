# Агент поддержки
# Пользователь пишет сообщение, агент определяет тип сообщения(жалоба, вопрос, благодарность)
# и в зависимости от типа сообщения отправляет его в 1 из 3 узлов
# каждый узел генерирует ответ в своем стиле
from langgraph.graph import StateGraph, START, END
from task2.schemas import (
    TypeMessage,
    StateAll,
    StateAfterReadPrompt,
    ResponseForQuestion,
    ResponseForGratitude,
    ResponseForComplaint,
)
from llm_model import llm_model


def read_user_prompt(state: StateAll):
    types_message: list[TypeMessage] = [t.value for t in TypeMessage]
    prompt = f"Пользователь пишет сообщение - {state['user_message']}. Определи по контексту его тип, из возможных {types_message} и запиши в словарь с ключом 'type_message'."
    structured_model_output = llm_model.with_structured_output(StateAfterReadPrompt)
    response = structured_model_output.invoke(prompt)
    return {
        "type_message": response.type_message,
    }


def response_for_question(state: StateAll):
    prompt = f"Пользователь написал сообщение с {state['type_message']}, вот само сообщение - {state['user_message']}. Проанализируй его и постарайся помочь решить проблему"
    structured_model_output = llm_model.with_structured_output(ResponseForQuestion)
    response = structured_model_output.invoke(prompt)
    return {"finally_response": response.finally_response}


def response_for_complaint(state: StateAll):
    prompt = f"Пользователь пишет с {state['type_message']} пишет {state['user_message']}. Помоги ему с вопросом."
    structured_model_output = llm_model.with_structured_output(ResponseForComplaint)
    response = structured_model_output.invoke(prompt)
    return {"finally_response": response.finally_response}


def response_for_gratitude(state: StateAll):
    prompt = f"Пользователь пишет с {state['type_message']} пишет {state['user_message']}. Помоги ему."
    structured_model_output = llm_model.with_structured_output(ResponseForGratitude)
    response = structured_model_output.invoke(prompt)
    return {"finally_response": response.finally_response}


def route_by_type(state: StateAll):
    if state["type_message"] == TypeMessage.complaint:
        return "response_for_complaint"
    if state["type_message"] == TypeMessage.question:
        return "response_for_questions"
    return "response_for_gratitude"


graph = (
    StateGraph(StateAll)
    .add_node("read_user_prompt", read_user_prompt)
    .add_node("response_for_complaint", response_for_complaint)
    .add_node("response_for_question", response_for_question)
    .add_node("response_for_gratitude", response_for_gratitude)
    .add_edge(START, "read_user_prompt")
    .add_conditional_edges("read_user_prompt", route_by_type)
    .add_edge("response_for_complaint", END)
    .add_edge("response_for_question", END)
    .add_edge("response_for_gratitude", END)
    .compile()
)
if __name__ == "__main__":
    result = graph.invoke(
        {
            "user_message": "Спасибо большое, ты мне помог разобраться с этой crud функцией алхимии"
        }
    )
    print(result)
