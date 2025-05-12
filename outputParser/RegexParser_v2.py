# -----------------------------------------------------
# 1) 필요한 클래스 임포트
# -----------------------------------------------------
from langchain.output_parsers import RegexParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# -----------------------------------------------------
# 2) 환경 변수 로딩
# -----------------------------------------------------
# .env 파일에서 OPENAI_API_KEY를 읽어 옵니다.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다.")

# -----------------------------------------------------
# 3) RegexParser 초기화
# -----------------------------------------------------
# - regex: "Name: <이름>, Age: <숫자>" 형태를 캡처
# - output_keys: 순서대로 "name", "age"라는 키로 결과를 매핑
parser = RegexParser(
    regex=r"Name:\s*(?P<name>\w+),\s*Age:\s*(?P<age>\d+)",
    output_keys=["name", "age"],
    default_output_key=None
)

# -----------------------------------------------------
# 4) 프롬프트 템플릿 준비
# -----------------------------------------------------
# LLM에게 응답을 "Name: 홍길동, Age: 30" 같은 형식으로 달라고 지시합니다.
prompt = PromptTemplate(
    template=(
        "아래 형식에 맞춰 응답해주세요:\n\n"
        "Name: <이름>, Age: <나이>\n\n"
        "질문: {query}"
    ),
    input_variables=["query"],
)

# -----------------------------------------------------
# 5) LLM 설정
# -----------------------------------------------------
# gpt-4o-mini 모델을 예시로 사용, verbose=True로 디버그용 프롬프트 확인 가능
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -----------------------------------------------------
# 6) 프롬프트와 LLM 결합 & 실행 + Parser도 파이프 연산자로 바로 적용
# -----------------------------------------------------
chain = prompt | llm | parser
# 예시 질의: "당신의 예시 이름과 나이를 알려주세요."
result = chain.invoke({"query": "당신의 예시 이름과 나이를 알려주세요."})
# 예시 raw_response == "Name: Alice, Age: 30"

# -----------------------------------------------------
# 8) 결과 확인
# -----------------------------------------------------
print(result)
# -> {'name': 'Alice', 'age': '30'}
print("이름:", result["name"])
print("나이:", result["age"])
