from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# print(gemini_api_key)


client = genai.Client(api_key=gemini_api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="대한민국의 수도는 어디야?",
)

print(response.text)