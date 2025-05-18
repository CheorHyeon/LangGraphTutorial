# =====================================================
# 0) 환경 변수 로딩
# =====================================================
# .env 파일에 저장된 OPENAI_API_KEY를 불러옵니다.
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일을 읽어 환경 변수로 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # API 키가 없으면 실행을 중단하고 에러를 출력합니다.
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# =====================================================
# 1) LLM 객체 생성
# =====================================================
# langchain_openai 패키지의 ChatOpenAI 클래스로 LLM 인스턴스를 만듭니다.
from langchain_openai import ChatOpenAI

# temperature=0 으로 설정하면 매번 동일한 답변을 얻도록 고정합니다.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# =====================================================
# 2) Few-Shot 예제 및 프롬프트 템플릿 정의
# =====================================================
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate

# 2-1) 예제 입력-출력 쌍을 리스트로 정의
examples = [
    {
        "question": "스티브 잡스와 아인슈타인 중 누가 더 오래 살았나요?",
        "answer": "아인슈타인"
    },
    {
        "question": "네이버의 창립자는 누구인가요?",
        "answer": "이해진"
    },
    {
        "question": "연산군은 어느 연도에 즉위했나요?",
        "answer": "1504년"
    }
]

# 2-2) 예제 하나를 출력할 때 사용할 포맷을 정의
#    {question}과 {answer} 자리에 실제 데이터를 넣어줍니다.
example_prompt = PromptTemplate(
    template="Question: {question}\nAnswer: {answer}",
    input_variables=["question", "answer"],
)

# 2-3) FewShotPromptTemplate 생성
#    - examples: 실제 예제 리스트
#    - example_prompt: 위에서 정의한 포맷, question과 answer를 어떤 형태로 넣을지 정의
#    - suffix: 모델에게 전달할 최종 프롬프트 끝부분, 모든 예제를 보여준 뒤 실제 사용자 질문을 받기 위해 붙이는 텍스트
#    - input_variables: 사용자 질문 변수 이름
#    - example_separator(선택) : 예제 사이 구분자 , 기본값운 \n\n / 변경 가능
#    - prefix(선택) : 예제 앞에 붙일 초기 지시문, 예제가 나오기 전 모델에게 태스크 설명 등을 미리 던질때 사용
few_shot_prompt = FewShotPromptTemplate(
    # prefix 옵션 추가
    prefix="다음 예시를 참고하여 질문에 답변해주세요.\n\n", # 생략 가능
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {question}\n",
    input_variables=["question"],
    example_separator="\n\n"  # 예제 사이 줄바꿈 두 줄로 구분, 기본값으로 생략 가능
)

# =====================================================
# 3) 출력 파서 및 GraphState 정의
# =====================================================
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel

# 3-1) GraphState 클래스
#    - state에 담길 데이터 구조를 정의합니다.
#    - question: 사용자 질문(필수)
#    - answer: 모델이 생성한 답변(초기값은 빈 문자열)
class GraphState(BaseModel):
    question: str
    answer: str = ""

# =====================================================
# 4) 노드 함수 정의: few_shot_node
# =====================================================
def few_shot_node(state: GraphState) -> dict:
    """
    1) Few-Shot 프롬프트 생성
    2) LLM 호출
    3) 문자열 출력 파싱
    4) 결과를 {'answer': ...} 형태로 반환
    """
    # 체인: few_shot_prompt → llm → StrOutputParser()
    chain = few_shot_prompt | llm | StrOutputParser()
    # invoke에 딕셔너리 형태로 입력을 넘겨줍니다.
    answer = chain.invoke({"question": state.question})
    # 상태의 answer 필드만 업데이트하기 위해 dict로 반환
    return {"answer": answer}

# =====================================================
# 5) StateGraph 구성 및 실행
# =====================================================
# 5-1) StateGraph 생성: 상태 스키마로 GraphState 사용
pipeline = StateGraph(GraphState)

# 5-2) 노드 추가
pipeline.add_node("few_shot", few_shot_node)

# 5-3) 시작(START) → few_shot → 끝(END) 연결
pipeline.add_edge(START, "few_shot")
pipeline.add_edge("few_shot", END)

# 5-4) 그래프 컴파일
graph = pipeline.compile()

# =====================================================
# 5) 사용자 입력 받기 및 결과 출력
# =====================================================
# 콘솔에 메시지를 띄우고, 사용자가 직접 질문을 입력하도록 함
user_question = input("👉 질문을 입력하세요: ")

# PromptTemplate이 조합한 전체 프롬프트 문자열 생성
full_prompt = few_shot_prompt.format(question=user_question)

# prefix, example1~N, suffix 순서대로 출력
print("\n===== 생성된 전체 프롬프트 =====")
print(full_prompt)
print("================================\n")

# GraphState 인스턴스를 생성해 그래프에 넘김
result = graph.invoke(GraphState(question=user_question))

# 최종 answer 출력
print("\n💡 답변:", result["answer"])