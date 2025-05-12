from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# =====================================================
# 0) 환경 변수 로딩
# =====================================================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다.")

# =====================================================
# 1) Pydantic 모델 정의
# =====================================================
# LLM의 응답을 구조화할 스키마를 Pydantic으로 선언
class Joke(BaseModel):
    setup: str = Field(..., description="농담의 질문 부분")
    punchline: str = Field(..., description="농담의 답변 부분")

# =====================================================
# 2) PydanticOutputParser 초기화
# =====================================================
# 위에서 만든 Joke 모델에 맞춰 LLM 출력을 파싱하도록 파서 생성 -> 내부적으로 `Joke.schema()`를 호출해 JSON 스키마를 얻음
## 어떤 키가 필요한지, 각 키의 타입은 무엇인지, 필수와 선택 필드 구분하는 format instructions 문자열 자동 생성
parser = PydanticOutputParser(pydantic_object=Joke)

# =====================================================
# 3) 프롬프트 템플릿 준비
# =====================================================
# get_format_instructions()를 통해 모델에 출력 형식을 지시하는 문자열을 PromptTemplate에 삽입
prompt = PromptTemplate(
    template=(
        "아래 형식에 맞춰 아래 질문에 응답해주세요:\n\n"
        "형식 : {format_instructions}\n"   # → JSON 스키마와 예시가 들어감
        "질문 : {query}"                   # → 실제 질문(프롬프트 본문)이 들어감
    ),
    # input_variables : 템플릿 문자열에 있는 변수와 비교하여 불일치하는 경우 예외 발생
    input_variables=["query"],
    # partial_variables : 항상 공통된 방식으로 가져오고 싶은 변수가 있는 경우
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# =====================================================
# 4) LLM(언어 모델) 설정
# =====================================================
# ChatOpenAI를 통해 실제 LLM 호출, 출력의 일관성을 위해 온도를 0으로 설정
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# =====================================================
# 5) 프롬프트와 LLM 결합 & 실행
# =====================================================
# LangChain의 파이프 연산자(|)를 이용해 PromptTemplate과 LLM을 연결
chain = prompt | llm | parser
# 실제 질의를 보내고 raw_output(LLM의 원시 응답)을 받아옵니다.
raw_output = chain.invoke({"query": "어린이가 좋아할 귀여운 농담을 하나 알려줘."})

# 프롬프트 출력 방법 -> PromptTemplate.format() 호출
print("[prompt] " + prompt.format(query="어린이가 좋아할 귀여운 농담을 하나 알려줘."))


# =====================================================
# 6) 파싱 및 결과 활용
# =====================================================

# 이제 setup과 punchline을 속성으로 바로 사용할 수 있습니다.
print("Q:", raw_output.setup)
print("A:", raw_output.punchline)
