# shot : 예시

from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types

client = genai.Client()

system_prompt = "너는 유치원 학생이야. 유치원생처럼 답변해줘."
prompt = "오리"

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt
    )
)

print(response.text)