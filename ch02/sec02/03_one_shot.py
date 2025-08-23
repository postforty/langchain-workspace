from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

system_instruction = "너는 유치원 학생이야. 유치원생처럼 답변해줘."

# one-shot
# - 예시 없이 프롬프트 작성
prompt = """
    USER: 참새
    MODEL: 짹짹
    USER: 오리
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction
    ),
    contents=prompt,
)

print(response.text)