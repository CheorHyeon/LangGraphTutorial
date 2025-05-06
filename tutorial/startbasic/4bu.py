# =============================================================================
# 4부: 인간 참여(Human-in-the-Loop) 예제 전체 코드
# =============================================================================
# 1) 기본 라이브러리 및 환경 변수 로드
from dotenv import load_dotenv        # .env 파일에서 API 키를 로드
import os                             # 환경 변수 접근용

# 메시지 타입, 도구, 체크포인터, 그래프 모듈
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_core.runnables.graph_ascii import draw_ascii

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt

# =============================================================================
# 1) 환경변수 로드
# =============================================================================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# =============================================================================
# 2) 상태(State) 타입 정의
# =============================================================================
class State(TypedDict):
    # 대화 히스토리를 누적하는 리스트
    messages: Annotated[list, add_messages]

# =============================================================================
# 3) 그래프 빌더 생성
# =============================================================================
builder = StateGraph(State)

# =============================================================================
# 4) 인간 지원 도구 정의 (@tool + interrupt)
# =============================================================================
@tool
def human_assistance(query: str) -> str:
    """
    - 이 도구는 사람의 승인이 필요할 때 사용됩니다.
    - interrupt() 호출 시 그래프가 중단되고, 외부에서 입력된 답변을 기다립니다.
    """
    # 그래프 실행 일시 중지 및 외부 입력 대기
    result = interrupt({"query": query})
    # 사용자(사람)가 제공한 'data' 필드를 반환
    return result["data"]

# =============================================================================
# 5) LLM 및 외부 도구 초기화
# =============================================================================
# 웹 검색용 도구 (TavilySearch)
search_tool = TavilySearch(max_results=2)
# 인간 지원 도구 포함
tools = [search_tool, human_assistance]
# ChatOpenAI 모델 초기화
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
# 도구를 LLM에 바인딩하여 tool_calls 기능 활성화
llm_with_tools = llm.bind_tools(tools)

# =============================================================================
# 6) 챗봇 노드 정의 및 등록
# =============================================================================
def chatbot_node(state: State) -> dict:
    """
    - State.messages 전체를 LLM에 전달합니다.
    - LLM이 tool_calls를 포함한 AIMessage를 반환할 수 있습니다.
    """
    msg = llm_with_tools.invoke(state.get("messages", []))
    # 중단점 도입 시 중복 호출 방지를 위해 tool_calls 최대 1개 제한
    assert len(msg.tool_calls) <= 1
    return {"messages": [msg]}

builder.add_node("chatbot", chatbot_node)

# =============================================================================
# 7) 도구 실행 노드 등록 (ToolNode)
# =============================================================================
tool_node = ToolNode(tools=tools)
builder.add_node("tools", tool_node)

# =============================================================================
# 8) 분기 설정: tool_calls 유무에 따라 tools 또는 종료로 이동
# =============================================================================
builder.add_conditional_edges(
    "chatbot",
    tools_condition,    # 마지막 AIMessage에 tool_calls가 있으면 "tools" 아니면 END
    {"tools": "tools", END: END}
)

# START → chatbot, tools → chatbot 으로 연결
builder.add_edge(START, "chatbot")
builder.add_edge("tools", "chatbot")

# =============================================================================
# 9) 체크포인터 설정 및 그래프 컴파일
# =============================================================================
# MemorySaver: 메모리 내 휘발성 체크포인터
memory = MemorySaver()
# 그래프 컴파일 시 checkpointer 옵션에 memory 전달
graph = builder.compile(checkpointer=memory)

# =============================================================================
# 10) 그래프 구조 시각화
# =============================================================================
internal = graph.get_graph()
vertices = {n: str(n) for n in internal.nodes}
edges = internal.edges
print("=== Graph Structure ===")
print(draw_ascii(vertices, edges))

# =============================================================================
# 11) 실행 예시: Human-in-the-Loop 워크플로우
# =============================================================================
# (1) 사용자 초기 입력
user_input = "I need some expert guidance for building an AI agent."

# (2) thread_id "1"로 그래프 실행 → human_assistance 호출 지시 후 중단
config = {"configurable": {"thread_id": "1"}}
events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for evt in events:
    # 도구 호출 지시가 있는 AIMessage 출력
    evt["messages"][-1].pretty_print()

# (3) 사람이 응답을 제공 → resume 명령 생성
human_response = (
    "We, the experts are here to help! "
    "I recommend checking out LangGraph's docs and examples."
)
resume_cmd = Command(resume={"data": human_response})

# (4) resume 명령으로 그래프 재개 → 최종 응답 생성
events = graph.stream(resume_cmd, config, stream_mode="values")
for evt in events:
    evt["messages"][-1].pretty_print()

# (5) 체크포인트 상태 확인
snapshot = graph.get_state(config)
print("[Snapshot]:", snapshot)
print("[Next nodes]:", snapshot.next)  # END에 도달 -> 빈 리스트([])