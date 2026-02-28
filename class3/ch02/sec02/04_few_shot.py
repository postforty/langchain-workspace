# 예제 2개 이상

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

system_instruction = "너는 유치원 학생이야. 유치원생처럼 답변해줘. 이모지, 특수 문자는 쓰지 말것!"

prompt = """
USER: 오리
MODEL: 꽥꽥
USER: 고양이
MODEL: 냐옹
USER: 강아지
MODEL: 멍멍
USER: 참새
"""

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction
    ),
    contents=prompt,
)

print(response.text)