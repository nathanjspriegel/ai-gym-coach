from langchain_core.messages import HumanMessage
from agent import get_agent
from tools import (
    log_exercise, 
    get_exercise_names, 
    get_personal_record, 
    get_today, 
    get_workout_history,
    get_exercise_progress,
)

def main():
    messages = []
    agent = get_agent()

    print("Hi! I'm your AI gym coach. How can I help you?")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("You: ").strip()
        if user_input == "quit":
            break

        messages.append(HumanMessage(content=user_input))

        print("\nAI: ", end="")
        for chunk in agent.stream({"messages": messages}): 
            if "model" in chunk:
                for message in chunk["model"]["messages"]:
                    print(message.content, end="")
                    messages.append(message)
            if "tools" in chunk:
                for message in chunk["tools"]["messages"]:
                    messages.append(message)
        print()



if __name__ == "__main__":
    main()