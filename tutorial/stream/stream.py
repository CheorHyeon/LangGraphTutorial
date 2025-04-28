from typing import TypedDict, Annotated
from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages

# =============================================================================
# State 타입 정의
# =============================================================================
class State(TypedDict):
    # 메시지 히스토리를 누적하기 위한 리스트
    messages: Annotated[list, add_messages]


# =============================================================================
# 노드 함수 정의
# =============================================================================
def add_greeting(state: dict) -> dict:
    """
    - START → greeting 노드 실행
    - 역할: AI 인삿말 추가
    """
    messages = state.get("messages", [])
    messages.append({"role": "ai", "content": "안녕하세요! 무엇을 도와드릴까요?"})
    return {"messages": messages}


def add_farewell(state: dict) -> dict:
    """
    - greeting → farewell 노드 실행
    - 역할: AI 작별인사 추가
    """
    messages = state["messages"]
    messages.append({"role": "ai", "content": "안녕히 계세요!"})
    return {"messages": messages}


# =============================================================================
# 그래프 빌드 함수
# =============================================================================
def build_graph() -> StateGraph:
    """
    StateGraph를 생성하고 START→greeting→farewell→END 순서로 노드를 연결한 후
    컴파일하여 반환합니다.
    """
    graph_builder = StateGraph(State)
    graph_builder.add_node("greeting", add_greeting)
    graph_builder.add_node("farewell", add_farewell)
    graph_builder.add_edge(START, "greeting")
    graph_builder.add_edge("greeting", "farewell")
    graph_builder.add_edge("farewell", END)
    return graph_builder.compile()


# =============================================================================
# main 함수: 스크립트로 실행될 때 동작
# =============================================================================
def main():
    # 1) 그래프 생성
    graph = build_graph()

    # 2) 입력 메시지 정의
    inputs = {
        "messages": [
            {"role": "human", "content": "안녕?"}
        ]
    }

    # 3) stream_mode 변경하며 각 단계별 상태 출력
    for chunk in graph.stream(inputs, stream_mode="debug"):
        print("DEBUG CHUNK:", chunk)

# =============================================================================
# 모듈을 직접 실행할 때만 main() 호출
# =============================================================================
if __name__ == "__main__":
    main()
