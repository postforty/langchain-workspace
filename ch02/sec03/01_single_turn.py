from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

system_instruction = "너는 사용자를 도와주는 상담사야."

while True:
    user_input = input("사용자: ")

    if user_input == "종료":
        break

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        ),
        contents=user_input,
    )

    print("AI상담사:", response.text)