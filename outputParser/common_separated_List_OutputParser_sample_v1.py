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
    template="{country}의 주요 도시 이름을 쉼표로 구분하여 나열해주세요.",
    input_variables=["country"],
)

# -----------------------------------------------------
# 5) LLM(언어 모델) 설정
# -----------------------------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -----------------------------------------------------
# 6) 프롬프트와 LLM 결합 & 실행
# -----------------------------------------------------
chain = prompt | llm
raw_output: str = chain.invoke({"country" : "대한민국"}).content

# 프롬프트 출력 방법 -> PromptTemplate.format() 호출
print("[prompt] " + prompt.format(country="대한민국"))

# -----------------------------------------------------
# 7) 파싱 실행
# -----------------------------------------------------
# 쉼표로 나누고 strip() 처리한 Python 리스트 반환
## parser.parse()에 LLM의 원시 문자열을 넘기면, 쉼표로 나눈 뒤 각 항목을 strip() 처리한 리스트가 반환됩니다.
## 내부적으로 raw_output.split(",") -> 항목별로 .strip() -> 최종적으로 List[str] 형태로 반환
cities: list[str] = parser.parse(raw_output)

# -----------------------------------------------------
# 8) 결과 확인
# -----------------------------------------------------
print(cities)
# 예시 출력 → ['서울', '부산', '인천', '대구', '대전', '광주', '울산', '수원', ...]
