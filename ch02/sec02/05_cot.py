from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

# Chain of Thought (CoT)
# 중간 추론 단계를 포함하여 모델이 복잡한 추론 문제를 해결할 수 있도록 도움
# few shot CoT
prompt = """
이 그룹의 홀수들을 합하면 짝수가 됩니다: 4, 8, 9, 15, 12, 2, 1.
A: 모든 홀수(9, 15, 1)를 더하면 25입니다. 정답은 False입니다.
이 그룹의 홀수들을 합하면 짝수가 됩니다: 17, 10, 19, 4, 8, 12, 24.
A: 모든 홀수(17, 19)를 더하면 36입니다. 정답은 True입니다.
이 그룹의 홀수들을 합하면 짝수가 됩니다: 15, 32, 5, 13, 82, 7, 1.
A: 
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt,
)

print(response.text)