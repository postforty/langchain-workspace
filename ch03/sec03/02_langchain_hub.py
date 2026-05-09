from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langsmith import Client
from dotenv import load_dotenv
load_dotenv()

client = Client()
prompt = client.pull_prompt("rlm/rag-prompt", dangerously_pull_public_prompt=True)

# print(prompt)

model = init_chat_model("google_genai:gemini-3.1-flash-lite")

chain = prompt | model | StrOutputParser()

context = "내 이름은 김일남이고, 나이는 99세이고, 아이스 아메리카노를 좋아해!"
question = "나는 몇 살일까?"

response = chain.invoke({"context": context, "question": question})

print(response)


