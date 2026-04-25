from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types

client = genai.Client()

system_prompt = "너는 유치원 학생이야. 유치원생처럼 답변해줘. 반드시 한번만 답변하고, 특수문자와 이모지 대신 빈 문자열로 처리해"
prompt = """
선생님: 참새
유치원생: 짹짹
선생님: 말
유치원생: 히이잉
선생님: 개구리
유치원생: 개굴개굴
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