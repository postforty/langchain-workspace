from langchain.chat_models import init_chat_model
from langchain_core.prompts import load_prompt
from dotenv import load_dotenv
load_dotenv()

model = init_chat_model("google_genai:gemini-3.1-flash-lite-preview")

version = "v1"

prompt_path = f"prompts/summary_{version}.yaml"

prompt_template = load_prompt(prompt_path, encoding="utf-8")

result = prompt_template.invoke("요약할 내용")

print(result)