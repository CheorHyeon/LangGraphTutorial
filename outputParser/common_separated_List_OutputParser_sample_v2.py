# -----------------------------------------------------
# 1) 필요한 클래스 임포트
# -----------------------------------------------------
from langchain_core.output_parsers.list import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# -----------------------------------------------------
# 2) 환경 변수 로딩
# -----------------------------------------------------
# .env 에서 OPENAI_API_KEY를 읽어 옵니다.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다.")

# -----------------------------------------------------
# 3) 파서 초기화
# -----------------------------------------------------
# 쉼표로 구분된 텍스트를 리스트로 변환해 주는 파서
parser = CommaSeparatedListOutputParser()

# -----------------------------------------------------
# 4) 프롬프트 템플릿 준비
# -----------------------------------------------------
# 대한민국의 주요 도시 이름을 “쉼표로 구분”하여 나열해 달라는 지시
prompt = PromptTemplate(
    template=
    "아래 형식에 맞춰 아래 질문에 응답해주세요:\n\n"
    "형식 : {format_instructions}\n"   # → JSON 스키마와 예시가 들어감
    "질문 : {query}"                   # → 실제 질문(프롬프트 본문)이 들어감
    ,
    # input_variables : 템플릿 문자열에 있는 변수와 비교하여 불일치하는 경우 예외 발생
    input_variables=["query"],
    # partial_variables : 항상 공통된 방식으로 가져오고 싶은 변수가 있는 경우
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# -----------------------------------------------------
# 5) LLM(언어 모델) 설정
# -----------------------------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -----------------------------------------------------
# 6) 프롬프트와 LLM, Parser 결합 & 실행
# -----------------------------------------------------
chain = prompt | llm | parser
print(chain.invoke({"query": "대한민국의 주요 도시 이름을 나열해주세요."}))

# 프롬프트 출력 방법 -> PromptTemplate.format() 호출
print("[prompt] " + prompt.format(query="대한민국의 주요 도시 이름을 나열해주세요."))
