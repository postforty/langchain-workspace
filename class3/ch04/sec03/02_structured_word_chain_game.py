import gradio as gr
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from typing import Literal, Optional

from dotenv import load_dotenv
load_dotenv()

class WordChainResponse(BaseModel):
    """끝말잇기 게임의 응답 구조"""
    word: str = Field(description="에이전트가 제시하는 다음 단어, 게임 종료 시에는 비워둡니다.")
    status: Literal["ongoing", "win", "lose"] = Field(description="게임의 현재 상태 (진행중, 유저 승리, 유저 패배)")
    reason: Optional[str] = Field(description="게임이 종료된 상세 이유 (예: '이미 나온 단어입니다.', '명사가 아닙니다.')")
    message: str = Field(description="사용자에게 보여줄 최종 메시지 (단어 또는 'YOU WIN!' 등)")

system_prompt="""당신은 끝말잇기 게임을 진행하는 AI 챗봇입니다.
지정된 WordChainResponse 형식에 맞춰 응답을 생성해야 합니다.

[게임 규칙]
1. 이미 나왔던 단어 재사용 금지
2. 두음법칙 허용 (리 -> 이)
3. 국어사전에 존재하는 단어만 가능
4. 명사만 가능
5. 한 글자 단어 금지
6. 유저가 규칙을 어기면 status를 'lose'로 하고 이유를 적으세요.
7. 당신이 단어를 잇지 못하면 status를 'win'으로 하세요.
8. 유저가 승리하면 message에 "YOU WIN!", 패배하면 "YOU LOSE!"를 포함하세요."""

agent = create_agent(
    model="google_genai:gemini-2.5-flash",
    tools=[],
    checkpointer=InMemorySaver(),
    system_prompt=system_prompt,
    response_format=WordChainResponse # 구조화된 출력 적용
)

def play_word_chain_game(message, history):
    """끝말잇기 게임 응답 함수"""
    response = agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        {"configurable": {"thread_id": "1"}}
    )

    game_data: WordChainResponse = response["structured_response"]

    print(game_data)

    if game_data.status == "ongoing":
        return game_data.word
    else:
        return f"{game_data.reason}\n\n{game_data.message}"

gr.ChatInterface(
    fn=play_word_chain_game,
    title="🤖구조화된 출력 끝말잇기 게임🤩",
    description="AI와 함께 끝말잇기 게임을 해보세요! 단어만 입력하면 됩니다."

).launch()