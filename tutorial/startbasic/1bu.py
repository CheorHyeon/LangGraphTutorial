# =============================================================================
# 1) 기본 라이브러리 임포트 & 환경변수 로드
# =============================================================================
from dotenv import load_dotenv
import os, openai

from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_core.runnables.graph_ascii import draw_ascii

# .env 파일에서 OPENAI_API_KEY 불러오기
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다.")

# =============================================================================
# 2) LLM(챗 모델) 초기화
# =============================================================================
# gpt-4o-mini 예시, 필요에 따라 model_name을 바꿔 주세요
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# =============================================================================
# 3) 상태(State) 타입 정의
# =============================================================================
class State(TypedDict):
    # messages는 리스트 형태, add_messages 로 내부 업데이트를 누적
    messages: Annotated[list, add_messages]

# =============================================================================
# 4) 챗봇 노드 함수 정의
# =============================================================================
def chatbot_node(state: State) -> dict:
    """
    State 타입의 사전(state) 입력을 받아서,
    llm.invoke 로 생성된 AI 응답 메시지를
    'messages' 리스트에 담아 반환합니다.
    """
    ai_message = llm.invoke(state["messages"])
    return {"messages": [ai_message]}

# =============================================================================
# 5) 그래프 빌더 설정
# =============================================================================
graph_builder = StateGraph(State)

# 5-1) 각 노드의 이름과 함수를 변수에 담아두면 명확합니다
NODE_CHATBOT = "chatbot"    
FUNC_CHATBOT = chatbot_node  

# 5-2) 노드 등록: (노드이름, 실행함수)
graph_builder.add_node(NODE_CHATBOT, FUNC_CHATBOT)

# 5-3) 시작점 → 챗봇 → 종료점 연결
graph_builder.add_edge(START, NODE_CHATBOT)
graph_builder.add_edge(NODE_CHATBOT, END)

# =============================================================================
# 6) 그래프 컴파일
# =============================================================================
# 컴파일 후에는 .run(), .stream() 등이 가능한 CompiledGraph 객체가 만들어집니다.
compiled_graph = graph_builder.compile()

# =============================================================================
# 7) 그래프 시각화 (ASCII 다이어그램)
# =============================================================================
# internal_graph: 실제 노드·에지 정보를 담고 있는 객체
internal_graph = compiled_graph.get_graph()

# vertices: {노드ID: 표시문자열}
vertices = {node: str(node) for node in internal_graph.nodes}

# edges: Edge 객체 리스트
edges = internal_graph.edges

print("=== Graph Structure ===")
print(draw_ascii(vertices, edges))

# =============================================================================
# 8) 실시간 채팅 루프 (스트리밍)
# =============================================================================
def stream_response(user_input: str):
    """
    사용자 입력 한 번마다 compiled_graph.stream() 으로
    AI의 응답을 중간중간 순차 출력합니다.
    """
    # 입력 형태를 딕셔너리로 포장
    input_payload = {"messages": [{"role": "user", "content": user_input}]}

    # stream() 은 각 실행 단계마다 이벤트(dict)를 반환
    for event in compiled_graph.stream(input_payload):
        # event 예시: {"chatbot": {"messages": [..., AIMessage]}"}
        values_view = event.values()                  # values_view == dict_values([ {"messages": [..., AIMessage]] }])
        updates_list = list(values_view)              # updates_list == [ {"messages": [..., AIMessage]] } ]
        update = updates_list[0]                      # {"messages": [...]} (직렬화 어려워서 리스트 거쳐서 꺼내옴)
        last_msg = update["messages"][-1].content     # 최신 AI 응답 텍스트
        print("Assistant:", last_msg)

# =============================================================================
# 9) 프로그램 진입점 정의
# =============================================================================
def main():
    print("\nType 'quit' to exit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        stream_response(user_input)

# =============================================================================
# 10) 직접 실행 시에만 main() 호출
# =============================================================================
if __name__ == "__main__":
    main()
