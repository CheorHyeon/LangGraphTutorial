# =====================================================
# 0) 환경 변수 로딩
# =====================================================
# .env 파일에 저장된 OPENAI_API_KEY를 불러옵니다.
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일을 읽어 환경 변수로 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# =====================================================
# 1) LLM 객체 생성
# =====================================================
# langchain_openai 패키지의 ChatOpenAI 클래스로 LLM 인스턴스를 만듭니다.
from langchain_openai import ChatOpenAI

# temperature=0 으로 설정하면 동일한 입력에 대해 항상 같은 답변을 얻을 수 있습니다.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# =====================================================
# 2) Few-Shot 예제 및 포맷 정의
# =====================================================
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate

# 2-1) 모델에게 보여줄 “예제 질문-응답” 리스트
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
    },
    {
        "question": "파이썬의 창시자는 누구인가요?",
        "answer": "귀도 반 로섬"
    },
    {
        "question": "세계 최초의 웹 브라우저 이름은?",
        "answer": "WorldWideWeb"
    }
]

# 2-2) 예제 하나를 어떻게 문자열로 만들지 포맷 정의
example_prompt = PromptTemplate(
    template="Question: {question}\nAnswer: {answer}",
    input_variables=["question", "answer"],
)

# =====================================================
# 3) ExampleSelector 생성 (길이 기반)
# =====================================================
from langchain_core.example_selectors.length_based import LengthBasedExampleSelector

# LengthBasedExampleSelector:
#  - examples: 사용할 전체 예제 리스트
#  - example_prompt: 각 예제를 포맷팅할 템플릿
#  - max_length: “예제 문자열 전체 길이(단어 기준)”이 이 값을 넘지 않도록 예제를 선택
#  - get_text_length : 길이 추출 방식 지정 가능
selector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    max_length=20,  # 단어수 (기본), get_text_length 지정하면 해당 함수대로 길이 추출
    # get_text_length=lambda txt: len(txt) ## 커스텀으로 길이 추출하는 방식 지정 가능
)

# =====================================================
# 4) FewShotPromptTemplate 생성 (selector 사용)
# =====================================================
few_shot_prompt = FewShotPromptTemplate(
    # ★ 여기서 examples 대신 example_selector를 전달합니다.
    example_selector=selector,
    example_prompt=example_prompt,
    # prefix: 예제들 앞에 붙일 “모델 지시문”
    prefix="아래 예시를 참고하여, 질문에 답변해주세요.\n\n",
    # suffix: 예제 뒤에 붙여서 실제 사용자 질문을 받을 자리
    suffix="Question: {question}\n",
    input_variables=["question"],
    example_separator="\n\n"  # 예제 사이에 빈 줄 2개로 구분
)

# =====================================================
# 5) 사용자 입력 받기 및 포맷된 프롬프트 확인
# =====================================================
# 터미널(콘솔)에서 질문을 직접 입력받습니다.
user_question = input("👉 질문을 입력하세요: ")

# FewShotPromptTemplate이 만들어 내는 “전체 프롬프트 문자열”
full_prompt = few_shot_prompt.format(question=user_question)

# prefix, 선택된 example1~N, suffix 순서로 출력됩니다.
print("\n===== 생성된 전체 프롬프트 =====")
print(full_prompt)
print("================================\n")

# =====================================================
# 6) LLM 호출 및 답변 출력
# =====================================================
from langchain_core.output_parsers import StrOutputParser

chain = few_shot_prompt | llm | StrOutputParser()

answer = chain.invoke({"question": user_question})

print("💡 답변:", answer)
