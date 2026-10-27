from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
from tools import log_exercise

load_dotenv()

def main():
    llm = ChatOpenAI(
        model = "gpt-4o-mini", 
        temperature=0
        )

    tools = [log_exercise]

    messages = []
    agent = create_agent(llm, tools)

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