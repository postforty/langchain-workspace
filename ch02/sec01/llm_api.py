from dotenv import load_dotenv
load_dotenv()

# import os
# print(os.getenv("GOOGLE_API_KEY"))

from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words in Korean",
)

print(response.text)