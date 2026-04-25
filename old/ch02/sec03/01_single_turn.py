# turn : 대화
# Single Turn : 대화 내용을 기억하지 않음

from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types

client = genai.Client()

system_prompt = "너는 사용자를 도와주는 상담사야."

while True:
    user_input = input("사용자: ")

    if user_input in ["exit", "종료"]:
        break

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )

    print("상담사: " + response.text)