from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types

client = genai.Client()

system_prompt = "너는 유치원 학생이야. 유치원생처럼 답변해줘."
prompt = """
선생님: 참새
유치원생: 짹짹
선생님: 오리
유치원생:
"""

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt
    )
)

print(response.text)