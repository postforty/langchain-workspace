from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

system_instruction = "너는 유치원 학생이야. 유치원생처럼 답변해줘."

# zero-shot
# 예시가 없음
prompt = "오리"

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction
    ),
    contents=prompt,
)

print(response.text)