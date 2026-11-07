from langchain_gigachat import GigaChat
from langchain.agents import create_agent
from config import settings
from schemas import GeneratePlanOutput, TripState

llm_model = GigaChat(
    model="GigaChat-2",
    verify_ssl_certs=False,
    credentials=settings.gigachat_credentials,
)

# Супер, фиксируем проект: агент-органайзер поездки. Вот весь путь по шагам (чтобы видеть, куда идём):

# State — что за данные "живут" в процессе.
# Узел generate_plan — одним вызовом модели придумывает список дней
# (без деталей, просто темы: "день 1 — приезд и центр города", "день 2 — музеи" и т.д.).
# Узел fill_day — берёт один конкретный день и просит модель наполнить его активностями.
# Условие — проверить, остались ли ещё дни без наполнения: если да → вернуться на fill_day для следующего дня,
# если нет → закончить.
# Собрать граф из этих узлов и условия.
# Запустить и посмотреть результат.
# # Шаг 1: State

# State — это данные, которые видит каждый узел и может изменить. Для нашей задачи нужно хранить:


# тему/город поездки (вход от пользователя, не меняется по ходу),
# список дней с их темой (результат узла 2),
# список дней уже с активностями — то, что мы постепенно наполняем (растёт по одному элементу за вызов fill_day),
# индекс, какой день по счёту сейчас обрабатываем (чтобы узел fill_day знал, кого брать следующим, и чтобы условие знало,
# когда остановиться).
def generate_plan(state: TripState):
    """
    Функция генерирует план по поездке, место и количество дней вводит пользователь.
    """
    prompt = f"Пользователь едет в {state['destination']} на {state['nums_day']}. Придумай тему для каждого дня поездки"
    model_with_structure = llm_model.with_structured_output(GeneratePlanOutput)
    result = model_with_structure.invoke(prompt)
    print(result)
    days_plan = [
        {"day_number": day.day_number, "theme": day.theme, "activities": []}
        for day in result.days
    ]
    return {"days_plan": days_plan}


state = {
    "destination": "Казань",
    "nums_day": 3,
    "days_plan": [],
    "current_day_index": 0,
}
if __name__ == "__main__":
    print(generate_plan(state=state))
