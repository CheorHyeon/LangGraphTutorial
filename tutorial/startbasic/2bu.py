# =============================================================================
# 1) 기본 라이브러리 임포트 & 환경변수 로드
#    - .env 파일에서 API 키를 불러와 환경 변수로 설정합니다.
# =============================================================================
from dotenv import load_dotenv
import os
import json

# LangChain/OpenAI, LangGraph, 도구 메시지 타입 등 필수 모듈
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langchain_core.runnables.graph_ascii import draw_ascii
from langchain_tavily import TavilySearch
from langgraph.types import StreamWriter

# .env 파일 읽기
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# =============================================================================
# 2) LLM(챗 모델) 초기화 및 도구 설정
#    - ChatOpenAI 모델을 streaming=False로 초기화합니다.
#    - 검색 도구(TavilySearch)를 생성하고 리스트에 담습니다.
# =============================================================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 예시 도구: TavilySearch
tool = TavilySearch(max_results=2)
tools = [tool]

# LLM에 도구 바인딩 (invoke 시 tool_calls 지원)
llm_with_tools = llm.bind_tools(tools)

# =============================================================================
# 3) 상태(State) 타입 정의
#    - TypedDict로 messages 리스트를 정의합니다.
#    - add_messages 어노테이션으로 자동 병합 처리.
# =============================================================================
class State(TypedDict):
    messages: Annotated[list, add_messages]

# =============================================================================
# 4) 그래프 빌드 및 노드 정의
# =============================================================================
graph_builder = StateGraph(State)

# 4.1) 챗봇 노드: LLM 호출만 처리
# 입력 State.messages를 받아 LLM 응답 메시지 추가
def chatbot_node(state: State) -> dict:
    # 단순 응답 메세지(AIMessage) 혹은 tool_calls 속성을 담은 AIMessage("이런 검색을 해달라" 같은 지시) 두가지 형태 중 한가지 내보내기 가능
    return {"messages": [llm_with_tools.invoke(state.get("messages", []))]}

graph_builder.add_node("chatbot", chatbot_node)

# 4.2) 도구 실행 노드: AIMessage 내 tool_calls 처리
class BasicToolNode:
    # 생성자(self는 생성된 인스턴스 자신으로 객체의 속성을 설정할 때 사용합니다.
    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    # 클래스 내부에서 정의된 메서드는 호출 시 self를 자동으로 전달합니다.
    # 클래스 변수 : 클래스 정의 블록 내 직접 할당한 변수 / 인스턴스 변수 : self를 통해 할당된 변수로 인스턴스별 고유 데이터 저장
    # __call__ 메서드 : 파이썬 인터프리터가 인스턴스를 함수 호출하듯 사용할 수 있도록 해줌
    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    # 파이썬 객체 -> json으로 직렬화
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

tool_node = BasicToolNode(tools)
# 노드가 실행될 때 tool_node(state) 형태 호출 -> __call__ 메서드 자동 실행됨
graph_builder.add_node("tools", tool_node)

# 4.3) 조건부 라우팅: chatbot 이후 도구 호출 여부에 따라 분기
def route_tools(state: State) -> str:
    last = state.get("messages", [])[-1]
    # tool_calls가 있으면 도구 노드로, 없으면 종료
    return "tools" if getattr(last, "tool_calls", None) else END

graph_builder.add_conditional_edges("chatbot", route_tools, {"tools": "tools", END: END})

# 4.4) 엣지 추가: START→chatbot, tools→chatbot
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")

# 그래프 컴파일
graph = graph_builder.compile()

# =============================================================================
# 5) 그래프 시각화 (ASCII 다이어그램)
# =============================================================================
# internal_graph: 실제 노드·에지 정보를 담고 있는 객체
internal_graph = graph.get_graph()

# vertices: {노드ID: 표시문자열}
vertices = {node: str(node) for node in internal_graph.nodes}

# edges: Edge 객체 리스트
edges = internal_graph.edges

print("=== Graph Structure ===")
print(draw_ascii(vertices, edges))

# =====================================₩========================================
# 6) 헬퍼: 사용자 입력을 받아 그래프 실행 및 스트리밍 출력
# =============================================================================
def stream_graph_updates(user_input: str):
    # 초기 상태 구성
    inputs = {"messages": [{"role": "human", "content": user_input}]}
    # values 모드로 각 단계 전체 상태 출력
    for chunk in graph.stream(inputs, stream_mode="values"):
        print("DEBUG CHUNK:", chunk)

# =============================================================================
# 7) main 함수: 대화 루프 실행
# =============================================================================
def main():
    user_input = input("User: ")
    stream_graph_updates(user_input)

# 모듈 직접 실행 시 main 호출
if __name__ == "__main__":
    main()
