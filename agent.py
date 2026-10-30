from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from tools import (
    log_exercise, 
    get_exercise_names, 
    get_personal_record, 
    get_today, 
    get_workout_history,
    get_exercise_progress,
)


load_dotenv()

def get_agent():
    llm = ChatOpenAI(
        model = "gpt-4o-mini", 
        temperature=0
        )

    tools = [
        log_exercise,
        get_exercise_names,
        get_personal_record,
        get_today,
        get_workout_history,
        get_exercise_progress,
    ]

    return create_agent(llm, 
            tools,
            system_prompt=(
                "You are a gym coach that logs workouts. "
                "Before logging any set, always call get_exercise_names first. " 
                "If the exercise name matches an existing name, like 'bench' matching 'Barbell Bench Press', "
                "then use the exact existing name."
            ),
    )