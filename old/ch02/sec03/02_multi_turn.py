# Multi Turn : 대화 내용을 기억

from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types

client = genai.Client()

system_prompt = "너는 사용자를 도와주는 상담사야."

chat = client.chats.create(
    model="gemini-3-flash-preview", 
    config=types.GenerateContentConfig(
            system_instruction=system_prompt
    )
)

while True:
    user_input = input("사용자: ")

    if user_input in ["exit", "종료"]:
        break

    response = chat.send_message(
        message=user_input
    )

    messages = chat.get_history()

    # for message in messages:
    #     print(f"{message.role}: {message.parts[0].text}")

    print("상담사: " + response.text)