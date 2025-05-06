# =============================================================================
# 1) 환경변수 로드
#    - .env 파일에서 API 키를 불러와 환경 변수로 설정합니다.
# =============================================================================
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# =============================================================================
# 2) 상태 타입 정의
#    - TypedDict로 messages, name, birthday 필드를 정의합니다.
#    - add_messages 어노테이션으로 메시지 리스트를 자동 병합 처리합니다.
# =============================================================================
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    birthday: str

# =============================================================================
# 3) 도구 정의: human_assistance
#    - 사용자 검토가 필요한 정보를 인간에게 묻기 위해 중단점(interrupt) 사용
#    - Command(update)로 상태를 갱신하는 패턴
# =============================================================================
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.types import Command, interrupt

@tool
def human_assistance(
    name: str,
    birthday: str,
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """
    인간 검토가 필요할 때 사용되는 도구입니다.
    interrupt() 호출 시 그래프가 멈추고 외부 입력을 기다립니다.
    """
    # 그래프 일시 중단: 사용자 응답 대기
    human_response = interrupt({
        "question": "Is this correct?",
        "name": name,
        "birthday": birthday,
    })

    # 검토 결과에 따라 상태 결정
    if human_response.get("correct", "").lower().startswith("y"):
        verified_name = name
        verified_birthday = birthday
        response = "Correct"
    else:
        verified_name = human_response.get("name", name)
        verified_birthday = human_response.get("birthday", birthday)
        response = f"Made a correction: {human_response}"

    # 상태 업데이트 및 ToolMessage 삽입
    state_update = {
        "name": verified_name,
        "birthday": verified_birthday,
        "messages": [
            ToolMessage(response, tool_call_id=tool_call_id)
        ],
    }
    return Command(update=state_update)

# =============================================================================
# 4) 노드 및 그래프 구성
#    - ChatOpenAI 모델과 검색/인간 지원 도구를 바인딩
#    - chatbot 노드, ToolNode, 조건부 분기 설정
#    - MemorySaver 체크포인터 사용
# =============================================================================
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# 도구 초기화
search_tool = TavilySearch(max_results=2)
tools = [search_tool, human_assistance]

# LLM에 도구 바인딩
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
llm_with_tools = llm.bind_tools(tools)

# 챗봇 노드 정의

def chatbot(state: State) -> dict:
    message = llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}

# 그래프 빌더 설정
builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools=tools))
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge(START, "chatbot")
builder.add_edge("tools", "chatbot")

# 체크포인터 설정 및 컴파일
t = MemorySaver()
graph = builder.compile(checkpointer=t)

# =============================================================================
# 5) 실행 흐름 예시
#    1) 사용자 질문 → 2) 검색 도구 호출 → 3) 인간 검토 도구 호출 →
#    4) 사용자 응답 재개 → 5) 최종 상태 확인
# =============================================================================
from langgraph.types import Command

user_input = (
    "Can you look up when LangGraph was released? "
    "When you have the answer, use the human_assistance tool for review."
)
config = {"configurable": {"thread_id": "1"}}

events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for evt in events:
    evt["messages"][-1].pretty_print()

# 사용자 응답을 재개하는 Command
human_command = Command(resume={
    "name": "LangGraph",
    "birthday": "Jan 17, 2024",
})
events = graph.stream(human_command, config, stream_mode="values")
for evt in events:
    evt["messages"][-1].pretty_print()

# 최종 상태 스냅샷 확인
snapshot = graph.get_state(config)
print({k: v for k, v in snapshot.values.items() if k in ("name", "birthday")})