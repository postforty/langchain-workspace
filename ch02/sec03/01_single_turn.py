# turn == 대화
# single-turn: 대화 내용을 기억하지 않음

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

system_instruction = "너는 사용자를 도와주는 상담사야."

while True:
    user_input = input("사용자: ")

    if user_input == "":
        break

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        ),
        contents=user_input,
    )

    print("AI:", response.text)