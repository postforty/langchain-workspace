from dotenv import load_dotenv
import os
import json
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain.chat_models import init_chat_model
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

load_dotenv()

PGVECTOR_ID = os.getenv("PGVECTOR_ID")
PGVECTOR_PW = os.getenv("PGVECTOR_PW")
PGVECTOR_HOST = os.getenv("PGVECTOR_HOST", "localhost")
PGVECTOR_PORT = os.getenv("PGVECTOR_PORT", "5432")
PGVECTOR_DB = os.getenv("PGVECTOR_DB")

connection = f'postgresql+psycopg://{PGVECTOR_ID}:{PGVECTOR_PW}@{PGVECTOR_HOST}:{PGVECTOR_PORT}/{PGVECTOR_DB}'

class PetBot:
    def __init__(self, conn):
        self.embedding_model = OllamaEmbeddings(model="bge-m3:latest")
        # self.llm = OllamaLLM(model="gemma3:1b")
        self.llm = init_chat_model("google_genai:gemini-2.5-flash-lite")
        self.vector_store = PGVector(
            collection_name="chat_history",
            connection=conn,
            embeddings=self.embedding_model,
        )
        self.output_parser = StrOutputParser()
        self.prompt = ChatPromptTemplate.from_template(
            """당신은 사용자와의 모든 대화 내용을 잘 기억하는 스마트 어시스턴트입니다.
주어진 문맥(과거에 저장된 기억)을 바탕으로 자연스럽게 대답하거나 질문에 답하세요.
정보가 상충한다면 가장 최신 정보를 우선하세요.

---
관련된 기억(문맥): {context}

---
사용자 입력: {question}
답변:
"""
        )
    
    def save_user_info(self, topic, content):
        doc = Document(page_content=content, metadata={"topic": topic})
        self.vector_store.add_documents([doc], ids=[topic])
        print(f"[{topic}] 정보가 최신화되었습니다: {content}")

    def get_user_context(self, question):
        docs = self.vector_store.similarity_search(question, k=2)
        context = "\n".join([doc.page_content for doc in docs])
        print("검색결과:" ,context)
        return context
    
    def run_petbot(self, question):
        related_docs = self.vector_store.similarity_search(question, k=3)
        existing_context = ""
        for d in related_docs:
            existing_context += f"- Topic ID [{d.metadata.get('topic', 'unkown')}]: {d.page_content}\n"
        
        intent_prompt = ChatPromptTemplate.from_template(
            """사용자의 입력문을 분석하여, 꼭 기억해 두어야 할 '새로운 사실'이거나 혹은 '기존 기억의 정정/수정'인지 판단하세요.
단순한 질문, 인사, 감탄사 등 보관할 필요가 없는 내용이라면 무시합니다.

[기존에 저장된 관련 기억들]
{existing_context}

[분석 규칙]
1. 사용자의 입력이 '기존에 저장된 관련 기억들'과 연관되어 있고 이전 내용을 정정하거나 업데이트하는 것이라면:
   - 해당하는 기존 기억의 'Topic ID'를 그대로 topic 필드에 유지하세요. (매우 중요: 일치해야 덮어쓰기 업데이트 됨)
   - content 필드에는 새롭게 업데이트된 내용을 완한 문장으로 적으세요.
2. 사용자의 입력이 처음 등장하는 '완전히 새로운 사실(정보)'이라면:
   - 의미를 잘 나타내는 영문 소문자와 언더스코어(_) 조합의 새로운 식별자를 만들어 topic 필드에 넣으세요 (예: user_hobby, fav_movie).
   - content 필드에는 기억해둘 사실을 완전한 문장으로 적으세요.
3. 사용자의 입력이 단순 질문이나 기억할 필요 없는 대화라면:
   - topic과 content 필드를 모두 빈 문자열("")로 반환하세요.

[출력 형식]
반드시 아래 JSON 형식으로만 응답하세요:
```json
{{"topic": "...", "content": "..."}}
```

사용자 입력: {question}
"""
        )

        intent_chain = intent_prompt | self.llm | StrOutputParser()
        intent_result = intent_chain.invoke({
            "existing_context": existing_context if existing_context.strip() else "저장된 관련 기억 없음",
            "question": question
        })

        try:
            clean_json = intent_result.replace("```json", "").replace("```", "").strip()
            extracted_info = json.loads(clean_json)

            topic = extracted_info.get("topic")
            content = extracted_info.get("content")

            if topic:
                self.save_user_info(topic, content)
                return f"[시스템 알림] 내용을 메모했습니다!\n- ID(주제): {topic}\n- 내용: {content}"
        except Exception as e:
            print(e)
        
        context = self.get_user_context(question)

        chain = (
            {
                "context": RunnableLambda(lambda x: context),
                "question": RunnablePassthrough()
            } 
            | self.prompt 
            | self.llm 
            | self.output_parser
        )

        answer = chain.invoke(question)
        return answer

if __name__ == "__main__":
    PGVECTOR_ID = os.getenv("PGVECTOR_ID")
    PGVECTOR_PW = os.getenv("PGVECTOR_PW")
    PGVECTOR_HOST = os.getenv("PGVECTOR_HOST", "localhost")
    PGVECTOR_PORT = os.getenv("PGVECTOR_PORT", "5432")
    PGVECTOR_DB = os.getenv("PGVECTOR_DB")

    connection = f'postgresql+psycopg://{PGVECTOR_ID}:{PGVECTOR_PW}@{PGVECTOR_HOST}:{PGVECTOR_PORT}/{PGVECTOR_DB}'

    petbot = PetBot(connection)

    print("펫봇과의 대화를 시작합니다. '종료'를 입력하면 대화가 끝납니다.")

    while True:
        user_question = input("사용자: ")
        if user_question in ["종료", "quit", "exit"]:
            print("대화를 종료합니다.")
            break

        bot_answer = petbot.run_petbot(user_question)
        print(f"펫봇: {bot_answer}")