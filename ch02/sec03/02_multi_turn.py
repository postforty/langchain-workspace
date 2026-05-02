# multi-turn: 대화 내용을 기억
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

system_instruction = "너는 사용자를 도와주는 친절한 상담사야."

chat = client.chats.create(model="gemini-2.5-flash-lite")

while True:
    user_input = input("사용자: ")

    if user_input in ["종료", "end", "exit", "그만", "quit"]:
        break

    response = chat.send_message(
        message=user_input
    )

    messages = chat.get_history()

    print("---")
    for message in messages:
        print(f"{message.role}: {message.parts[0].text}")
    print("---")

    print("AI:", response.text)