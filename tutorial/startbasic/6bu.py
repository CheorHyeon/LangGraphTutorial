# =============================================================================
# 1) 환경변수 로드
#    - .env 파일에서 API 키를 불러와 환경 변수로 설정합니다.
# =============================================================================
from dotenv import load_dotenv
import os

# .env 파일 읽기
load_dotenv()
# OPENAI/MODEL API 키 환경 변수에서 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# =============================================================================
# 2) 상태(State) 타입 정의
#    - TypedDict로 messages 리스트를 정의합니다.
#    - add_messages 어노테이션으로 메시지들이 자동으로 누적되도록 설정.
# =============================================================================
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    # 대화 히스토리를 누적하는 리스트
    messages: Annotated[list, add_messages]

# =============================================================================
# 3) 노드 및 도구 초기화
#    - Chat 모델과 검색 도구를 초기화하고 바인딩합니다.
# =============================================================================
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition

# 3.1) 검색 도구 생성 (TavilySearch)
search_tool = TavilySearch(max_results=2)
# 등록할 도구 리스트
tools = [search_tool]

# 3.2) ChatOpenAI 모델 초기화 및 도구 바인딩
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
llm_with_tools = llm.bind_tools(tools)

# 3.3) chatbot 노드: 대화 히스토리를 받아 LLM 호출 결과를 메시지로 반환
def chatbot(state: State) -> dict:
    # state["messages"] 안에 누적된 Human/AI/Tool 메시지를 LLM에 전달
    reply = llm_with_tools.invoke(state["messages"])
    return {"messages": [reply]}

# =============================================================================
# 4) 그래프 빌드
#    - StateGraph에 노드와 엣지를 정의하고 체크포인터를 설정합니다.
# =============================================================================
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

# 4.1) 그래프 빌더 생성
builder = StateGraph(State)
# 4.2) 노드 등록: chatbot, tools
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools=tools))
# 4.3) 분기 설정: chatbot 후 도구 호출 여부에 따라 tools 또는 END
builder.add_conditional_edges("chatbot", tools_condition)
# 4.4) 엣지 연결: START→chatbot, tools→chatbot
builder.add_edge(START, "chatbot")
builder.add_edge("tools", "chatbot")

# 4.5) 휘발성 메모리 체크포인터 설정
memory = MemorySaver()
# 4.6) 그래프 컴파일
graph = builder.compile(checkpointer=memory)

# =============================================================================
# 5) 시간여행 예시: 두 차례 대화 후 상태 기록
#    - get_state_history를 이용해 스냅샷들을 순회
# =============================================================================
config = {"configurable": {"thread_id": "1"}}

# 첫 번째 사용자 질문 실행
events = graph.stream(
    {"messages": [{"role": "user", "content": "I'm learning LangGraph. Could you do some research on it for me?"}]},
    config,
    stream_mode="values"
)
for evt in events:
    evt["messages"][-1].pretty_print()

# 두 번째 사용자 질문 실행
events = graph.stream(
    {"messages": [{"role": "user", "content": "Ya that's helpful. Maybe I'll build an autonomous agent with it!"}]},
    config,
    stream_mode="values"
)
for evt in events:
    evt["messages"][-1].pretty_print()

# =============================================================================
# 6) 체크포인트 기록 확인 및 재생할 시점 선택
#    - get_state_history로 이전 스냅샷을 나열
#    - 대화 메시지 수로 특정 스냅샷 선택
# =============================================================================

to_replay = None
# 전체 히스토리 순회: 각 StateSnapshot 객체
for snapshot in graph.get_state_history(config):
    count = len(snapshot.values["messages"])
    print(f"Num Messages: {count}, Next node: {snapshot.next}")
    # 예: 메시지 6개일 때 다시 시작하고 싶다면
    if count == 6:
        to_replay = snapshot

# 재생할 스냅샷 정보 확인
print("Replaying from next node:", to_replay.next)
print("Use config:", to_replay.config)

# =============================================================================
# 7) 시간여행: 선택한 스냅샷으로 그래프 재실행
#    - to_replay.config에 담긴 checkpoint_id를 사용
#    - stream(None, to_replay.config) 으로 과거부터 다시 진행
# =============================================================================
for evt in graph.stream(None, to_replay.config, stream_mode="values"):
    evt["messages"][-1].pretty_print()