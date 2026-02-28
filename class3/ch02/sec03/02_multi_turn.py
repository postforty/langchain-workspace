# multi-turn: 대화 내용을 기억

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

system_instruction = "너는 사용자를 도와주는 상담사야."

chat = client.chats.create(model="gemini-3-flash-preview")

while True:
    user_input = input("사용자: ")

    if user_input == "":
        break

    messages = chat.get_history()

    print("messages 타입:", type(messages))
    print("messages 내용:", messages)

    response = chat.send_message(message=user_input)

    print("AI:", response.text)