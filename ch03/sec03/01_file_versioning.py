from langchain.chat_models import init_chat_model
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

def run_summary(version, text):
    model = init_chat_model("google_genai:gemini-3.1-flash-lite")

    prompt_path = f"prompts/summary_{version}.yaml"

    prompt_template = load_prompt(prompt_path, encoding="utf-8")

    # result = prompt_template.invoke("요약할 내용")

    output_parser = StrOutputParser()

    chain = prompt_template | model | output_parser

    print(f"--- 프롬프트 {version} 버전 ---")

    response = chain.invoke({"text": text})
    print(response)

if __name__ == "__main__":
    sample_text = """Agents combine language models with tools to create systems that can reason about tasks, decide which tools to use, and iteratively work towards solutions.
create_agent provides a production-ready agent implementation.
An LLM Agent runs tools in a loop to achieve a goal. An agent runs until a stop condition is met - i.e., when the model emits a final output or an iteration limit is reached."""

    run_summary("v1", sample_text)

    print("---")

    run_summary("v2", sample_text)