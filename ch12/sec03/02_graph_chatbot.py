from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

model = init_chat_model(
    "google_genai:gemini-2.5-flash",
    temperature = 0
)

def chat_node(state: MessagesState):
    response = model.invoke(state['messages'])
    return {'messages': [response]}

graph_builder = StateGraph(MessagesState)

graph_builder.add_node("chat",  chat_node)

graph_builder.add_edge(START, "chat")
graph_builder.add_edge("chat", END)

graph = graph_builder.compile()

def run_chatbot():
    print("Chatbot 시작! (종료: exit)")

    state: MessagesState  = {"messages": []}

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit"]:
            print("Chatbot 종료!")
            break

        if not user_input:
            continue

        user_msg = HumanMessage(content=user_input)
        state["messages"].append(user_msg)

        result_state = graph.invoke(state)

        new_messages = result_state["messages"]

        ai_msg = new_messages[-1]

        print(f"AI: {ai_msg.content}")

        state["messages"].append(ai_msg)

if __name__ == "__main__":
    run_chatbot()