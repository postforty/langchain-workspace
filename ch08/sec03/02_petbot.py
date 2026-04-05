from dotenv import load_dotenv
import os
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
            """주어진 과거 대화 기록을 참고하여 질문에 답변해 주세요.
과거 대화 기록이 질문과 관련 없다면 무시하세요.

---
과거 대화 기록: {context}

---
질문: {question}
답변:
"""
        )
    
    def save_chat_history(self, question, answer):
        chat_log = f"사용자: {question}\n챗봇: {answer}"
        doc = Document(page_content=chat_log)
        self.vector_store.add_documents([doc])
        print("대화 기록이 벡터 DB에 저장되었습니다.")
    
    def get_related_history(self, question):
        docs = self.vector_store.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        print("검색결과:" ,context)
        return context
    
    def run_petbot(self, question):
        context = self.get_related_history(question)
        print("--- 과거 대화 기록 검색 완료 ---")

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

        self.save_chat_history(question, answer)

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