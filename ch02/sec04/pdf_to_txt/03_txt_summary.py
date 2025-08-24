from google import genai
import os
from dotenv import load_dotenv # uv add python-dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# print(gemini_api_key)

def summarize_txt(file_path: str):
    client = genai.Client(api_key=gemini_api_key) # Gemini API와 통신하기 위한 클라이언트 객체 생성

    file_ref = client.files.upload(file=file_path)

    system_prompt = f'''
    이 글을 읽고, 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약하라.
    작성해야 하는 포맷은 다음과 같다.

    # 제목

    ## 저자의 문제 인식 및 주장 (15문장 이내)

    ## 저자 소개
    '''

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[file_ref, system_prompt]
    )

    return response.text

file_path = r"D:\wsh\langchain-workspace\ch02\sec04\pdf_to_txt\output\result_pymupdf.txt"

summary = summarize_txt(file_path)
print(summary)