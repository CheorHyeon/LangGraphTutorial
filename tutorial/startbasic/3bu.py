# =============================================================================
# 파트 3: 챗봇에 메모리 추가 (MemorySaver)
# =============================================================================
from dotenv import load_dotenv
import os

from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.runnables.graph_ascii import draw_ascii

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

# =============================================================================
# 1) 환경변수 로드
# =============================================================================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# =============================================================================
# 2) 메모리 및 상태 정의
#    - MemorySaver: 메모리 내 체크포인트
#    - State: 대화 메시지를 누적
# =============================================================================
# 매번 스크립트 실행할 때 새 인스턴스 생성 -> 프로그램 종료와 함께 초기화
## 영속성 메모리 필요할때 영속 스토리지를 백엔드로 사용하는 체크포인터를 사용해야 함
## SqliteSave or PostgresSaver
memory = MemorySaver()

class State(TypedDict):
    messages: Annotated[list, add_messages]

# =============================================================================
# 3) LLM 및 도구 초기화
# =============================================================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
search_tool = TavilySearch(max_results=2)
tools = [search_tool]
# LLM에 도구 바인딩
llm_with_tools = llm.bind_tools(tools)

# =============================================================================
# 4) 그래프 빌드
#    - chatbot 노드: 사용자 메시지를 LLM에 전달
#    - tools 노드: ToolNode 사용
#    - 조건부 분기: tools_condition
# =============================================================================
builder = StateGraph(State)

# 4.1) 챗봇 노드 등록
def chatbot_node(state: State) -> dict:
    response = llm_with_tools.invoke(state.get("messages", []))
    return {"messages": [response]}
builder.add_node("chatbot", chatbot_node)

# 4.2) 도구 노드 등록 (prebuilt ToolNode)
## ToolNode : LLM이 tool_calls 속성을 담은 AIMessage 반환 시 ToolNode가 메시지를 읽어 각 호출 지시에 맞춰 실제 도구 실행
## 결과를 ToolMessage 형태로 포장해서 state["messages"]에 돌려줌
tool_node = ToolNode(tools=tools)
builder.add_node("tools", tool_node)

# 4.3) 조건부 분기 설정
builder.add_conditional_edges(
    "chatbot",
    tools_condition, # chatbot 노드가 반환한 state 안의 마지막 메시지에 tool_calls가 존재하면 tools 없으면 END
    {"tools": "tools", END: END}
)

# 4.4) 엣지 연결: START→chatbot, tools→chatbot
builder.add_edge(START, "chatbot")
builder.add_edge("tools", "chatbot")

# 그래프 컴파일 (MemorySaver 체크포인터 포함)
graph = builder.compile(checkpointer=memory)

# =============================================================================
# 5) 그래프 구조 시각화
# =============================================================================
internal = graph.get_graph()
vertices = {n: str(n) for n in internal.nodes}
edges = internal.edges
print("=== Graph Structure ===")
print(draw_ascii(vertices, edges))

# =============================================================================
# 6) 메모리 테스트: 멀티턴 대화 예시
# =============================================================================
# Thread '1'에서 첫 입력
config1 = {"configurable": {"thread_id": "1"}}
events = graph.stream(
    {"messages": [{"role": "user", "content": "Hi there! My name is Will."}]},
    config1,
    stream_mode="values",
)
for evt in events:
    evt["messages"][-1].pretty_print()

# 같은 Thread에서 두 번째 입력: 사용자 이름 기억 여부 확인
events = graph.stream(
    {"messages": [{"role": "user", "content": "Remember my name?"}]},
    config1,
    stream_mode="values",
)
for evt in events:
    evt["messages"][-1].pretty_print()

# Thread '2'에서는 메모리가 초기화됨 (다른 Thread)
config2 = {"configurable": {"thread_id": "2"}}
events = graph.stream(
    {"messages": [{"role": "user", "content": "Remember my name?"}]},
    config2,
    stream_mode="values",
)
for evt in events:
    evt["messages"][-1].pretty_print()

# =============================================================================
# 7) 체크포인트 상태 확인
# =============================================================================
snapshot = graph.get_state(config1)
print("[Snapshot]", snapshot)
print("[Next Node]", snapshot.next)