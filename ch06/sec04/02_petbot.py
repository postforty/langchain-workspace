from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

class PetBot:
    def __init__(self, connection):
        self.embedding_model = OllamaEmbeddings(model="bge-m3", base_url="http://localhost:11434")
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                            google_api_key=gemini_api_key)

        self.vector_store = PGVector(
            collection_name="chat_history", # 대화 기록을 저장할 컬렉션(대화 세션의 고유한 식별자)
            embeddings=self.embedding_model,
            connection=connection,
        )
        self.output_parser = StrOutputParser()

        from langchain_core.prompts import ChatPromptTemplate

        self.prompt = ChatPromptTemplate.from_template(
            '''
            주어진 과거 대화 기록을 참고하여 질문에 답변해 주세요.
            과거 대화 기록이 질문과 관련 없다면 무시하세요.

            컨텍스트:{context}

            질문:{question}
            답변:
            '''
        )
    
    def save_chat_history(self, question, answer):
        """사용자의 질문과 챗봇의 답변을 벡터 DB에 저장."""
        chat_log = f"사용자: {question}\n챗봇: {answer}"
        doc = Document(page_content=chat_log) # 비정형 텍스트 데이터를 정형화된 문서 객체로 반환
        self.vector_store.add_documents([doc])
        print("대화 기록이 벡터 DB에 저장되었습니다.")

    def get_related_history(self, question):
        """새 질문과 관련된 과거 대화 기록을 검색"""
        docs = self.vector_store.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        return context

    def run_petbot(self, question):
        """챗봇 실행 로직: 검색 -> 답변 -> 기록 저장"""

        context = self.get_related_history(question)
        print("---과거 대화 기록 검색 완료---")

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

# 민감한 정보를 감추기 위해 환경변수 처리
PGVECTOR_ID = os.getenv("PGVECTOR_ID")
PGVECTOR_PW = os.getenv("PGVECTOR_PW")
PGVECTOR_DB = os.getenv("PGVECTOR_DB")
PGVECTOR_HOST = os.getenv("PGVECTOR_HOST")
PGVECTOR_PORT = os.getenv("PGVECTOR_PORT")

connection = f"postgresql+psycopg://{PGVECTOR_ID}:{PGVECTOR_PW}@{PGVECTOR_HOST}:{PGVECTOR_PORT}/{PGVECTOR_DB}"

petbot = PetBot(connection)

print("펫봇과 대화를 시작합니다. '종료'를 입력하면 대화가 끝납니다.")

while True:
    user_question = input("사용자: ")

    if user_question == "종료":
        print("대화를 종료합니다.")
        break
    
    bot_answer = petbot.run_petbot(user_question)
    print(f"펫봇: {bot_answer}")
    