from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

chat = client.chats.create(model="gemini-2.5-flash") # 대화 내용 기억하기 위해 추가

while True:
    user_input = input("사용자: ")

    if user_input == "종료":
        break

    response = chat.send_message(
        message=user_input
    ) # 수정

    messages = chat.get_history() # 추가

    # print(messages)

    print("AI상담사:", response.text)