from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

prompt_basic = """
시장에 가서 사과 10개를 샀습니다. 이웃에게 2개, 수리 기사님께 2개를 나누어 주었습니다.
그 후 사과 5개를 더 사고 1개를 먹었습니다. 남은 사과는 총 몇 개인가요?
추론 과정  없이 최종 숫자만 답변하세요.
"""

prompt_zero_shot_cot = """
시장에 가서 사과 10개를 샀습니다. 이웃에게 2개, 수리 기사님께 2개를 나누어 주었습니다.
그 후 사과 5개를 더 사고 1개를 먹었습니다. 남은 사과는 총 몇 개인가요?
차근차근 단계별로 생각해보세요.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt_basic,
)
print(response.text)

print("---")

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt_zero_shot_cot,
)
print(response.text)