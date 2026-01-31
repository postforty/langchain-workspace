from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_postgres import PGVector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os
from dotenv import load_dotenv
load_dotenv()

class PetBot:
    def __init__(self, connection_str):
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )
        self.llm = init_chat_model("google_genai:gemini-2.5-flash")
        self.vector_store = PGVector(
            collection_name="chat_history",
            embeddings=self.embedding_model,
            connection=connection_str,
        )
        self.output_parser = StrOutputParser()
        self.prompt = ChatPromptTemplate.from_template(
            """주어진 과거 대화 기록을 참고하여 질문에 답변해 주세요.
과거 대화 기록을 반드시 언급하고 답변을 해주세요.

---
과거 대화 기록: {context}

---
질문: {question}
답변:
"""
        )
    
    def save_chat_history(self, question, answer):
        chat_log = f"사용자: {question}\n\n챗봇: {answer}"
        doc = Document(page_content=chat_log)
        self.vector_store.add_documents([doc])
        # print("대화 기록이 벡터 DB에 저장되었습니다.")
    
    def get_related_history(self):
        retriver = self.vector_store.as_retriever(k=3)
        return retriver
    
    def run_petbot(self, question):
        chain = (
            {
                "context": self.get_related_history(),
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
    PGVECTOR_HOST = os.getenv("PGVECTOR_HOST")
    PGVECTOR_PORT = os.getenv("PGVECTOR_PORT")
    PGVECTOR_DB = os.getenv("PGVECTOR_DB")

    connection_str=f"postgresql+psycopg://{PGVECTOR_ID}:{PGVECTOR_PW}@{PGVECTOR_HOST}:{PGVECTOR_PORT}/{PGVECTOR_DB}"

    petBot = PetBot(connection_str)

    while True:
        user_question = input("👨사용자: ")

        if user_question in ["exit", "종료", "끝", "end"]:
            break;
         
        bot_answer = petBot.run_petbot(user_question)
        print("🤖펫봇:", bot_answer)
