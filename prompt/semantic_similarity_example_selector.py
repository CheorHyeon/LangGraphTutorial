# =====================================================
# 0) 라이브러리 임포트 및 환경 변수 로딩
# =====================================================
from dotenv import load_dotenv             # .env 파일에서 환경 변수를 읽어오는 모듈
import os                                  # 운영체제 환경 변수를 다루는 모듈

# OpenAI 결과를 문자열로 파싱하는 도구
from langchain_core.output_parsers import StrOutputParser
# Few-Shot Prompt 구성에 필요한 템플릿 클래스
from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate
)

from langchain_core.example_selectors import (
        SemanticSimilarityExampleSelector
)

# .env 파일을 읽어들여 환경 변수를 설정
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")


# =====================================================
# 1) OpenAI 임베딩 및 LLM 객체 생성
# =====================================================
# 임베딩 모델: 텍스트를 고정 길이 벡터(숫자 배열)로 변환
# 가장 저렴한 'text-embedding-3-small' 모델 사용
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# LLM: 실제 프롬프트를 입력받아 답변을 생성
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# temperature=0 으로 설정하면, 동일한 프롬프트에 대해 항상 같은 결과를 얻습니다.


# =====================================================
# 2) ChromaDB 클라이언트 초기화
# =====================================================
# Chroma: 파이썬 라이브러리 형태의 벡터 데이터베이스
# - 별도 서버 없이 로컬(메모리 또는 디스크)에 벡터를 저장하고
#   빠른 유사도 검색을 지원합니다.
from langchain_chroma import Chroma

# Vector DB 생성 (저장소 이름, 임베딩 클래스)
chroma_collection = Chroma("example_selector", embeddings)

# =====================================================
# 3) 예제(question-answer) 목록 및 포맷 정의
# =====================================================
# 3-1) 모델에게 보여줄 “예제 질문-응답” 리스트
examples = [
    {"question": "스티브 잡스와 아인슈타인 중 누가 더 오래 살았나요?", "answer": "아인슈타인"},
    {"question": "네이버의 창립자는 누구인가요?",              "answer": "이해진"},
    {"question": "연산군은 어느 연도에 즉위했나요?",            "answer": "1504년"},
    {"question": "파이썬의 창시자는 누구인가요?",             "answer": "귀도 반 로섬"},
    {"question": "세계 최초의 웹 브라우저 이름은?",            "answer": "WorldWideWeb"},
]

# 3-2) 예제 하나를 문자열로 만들 때 사용할 템플릿
#    {question}과 {answer} 자리에 실제 값을 대입합니다.
example_prompt = PromptTemplate(
    template="Question: {question}\nAnswer: {answer}",
    input_variables=["question", "answer"],
)

# =====================================================
# 4) SemanticSimilarityExampleSelector 설정
# =====================================================
# SemanticSimilarityExampleSelector:
# - 미리 저장한 예제 벡터들과 사용자 질문 벡터를 비교해
#   의미적으로 가장 유사한 예제 k개를 자동으로 골라주는 도구.

example_selector = SemanticSimilarityExampleSelector.from_examples(
    # 선택 가능한 예시 목록
    examples,
    # 의미적 유사성을 측정하는 데 사용되는 임베딩을 생성하는 임베딩 클래스
    embeddings,
    # 임베딩을 저장하고 유사성 검색을 수행하는 데 사용되는 VectorStore 클래스
    ## Chroma로 사용 - from_examples 내부에서 Chroma("example_selector", embeddings)를 자동으로 생성하여 벡터 저장소 세팅
        ## vectorstore_cls: type[VectorStore] 이기 때문에 노란줄 안뜸
        ## 하지만 명시적으로 인스턴스를 지정하면 노란줄 뜸 -> 런타임 시 호출 가능하면 내부에서 실행하려 시도 -> 오류x
    chroma_collection,
    # 이것은 생성할 예시의 수입니다.
    k=1,
)


# =====================================================
# 5) Few-Shot PromptTemplate에 selector 연결
# =====================================================
# FewShotPromptTemplate:
# - example_selector: 위에서 만든 selector 사용 → 자동으로 k개 예제 검색
# - example_prompt: 3-2)에서 정의한 포맷
# - prefix: 예제들 앞에 붙일 “지시문”
# - suffix: 예제 뒤에 “실제 질문 자리”
# - example_separator: 예제 간 구분 문자
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="아래 예시와 비슷한 한 가지 예시를 참고해 질문에 답변해주세요.\n\n",
    suffix="Question: {question}\nAnswer:",
    input_variables=["question"],
    example_separator="\n\n"
)


# =====================================================
# 6) 사용자 입력 받아 실행 및 결과 출력
# =====================================================
# 6-1) 콘솔에서 질문 입력 받기
user_question = input("👉 질문을 입력하세요: ")

# 6-2) Few-Shot Prompt 전체 문자열 확인 (디버그용)
print("\n=== 생성된 Prompt ===")
print(few_shot_prompt.format(question=user_question))
print("=====================\n")

# 6-3) LLM 호출 후, 문자열만 추출해 출력
chain = few_shot_prompt | llm | StrOutputParser()
answer = chain.invoke({"question": user_question})

print("💡 답변:", answer)
