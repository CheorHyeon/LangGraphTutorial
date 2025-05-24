# =====================================================
# 1) 라이브러리 불러오기
# =====================================================
import time
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
from langchain_community.cache import SQLiteCache

# =====================================================
# 2) 환경 변수 로딩 & API 키 검증
# =====================================================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다.")

# =====================================================
# 3) LLM 모델 초기화
# =====================================================
# gpt-4.1-mini 모델을 사용합니다
llm = ChatOpenAI(model="gpt-4.1-mini")

# =====================================================
# 4) 공통 프롬프트 & 체인 정의
# =====================================================
# “{country}에 대해서 200자 내외로 요약해줘” 라는 템플릿
prompt = PromptTemplate(
    template="{country}에 대해서 200자 내외로 요약해줘",
    input_variables=["country"]
)
# 프롬프트 → LLM → 문자열 출력 파서
chain = prompt | llm | StrOutputParser()

# =====================================================
# 5) 1) 단순 모델 호출 예제
# =====================================================
print("\n--- 1) 단순 모델 호출 ---")
response = chain.invoke({"country": "한국"})
print("응답:", response)

# =====================================================
# 6) 2) InMemoryCache 테스트
# =====================================================
print("\n--- 2) InMemoryCache 테스트 ---")
# 전역 캐시로 InMemoryCache 설정
set_llm_cache(InMemoryCache())

# 첫 번째 호출 (캐시 미스)
start = time.perf_counter()
resp1 = chain.invoke({"country": "한국"})
t1 = time.perf_counter() - start
print("첫 호출 응답:", resp1)
print(f"첫 호출 소요 시간: {t1:.3f}초")

# 두 번째 호출 (캐시 히트)
start = time.perf_counter()
resp2 = chain.invoke({"country": "한국"})
t2 = time.perf_counter() - start
print("두 번째 호출 응답:", resp2)
print(f"두 번째 호출 소요 시간: {t2:.3f}초")

# =====================================================
# 7) 3) SQLiteCache 테스트
# =====================================================
print("\n--- 3) SQLiteCache 테스트 ---")
# 캐시 파일 저장 디렉토리 생성
os.makedirs("cache", exist_ok=True)
# 전역 캐시로 SQLiteCache 설정
set_llm_cache(SQLiteCache(database_path="cache/llm_cache.db"))

# 첫 번째 호출 (DB에 캐시 없음 → 느림)
start = time.perf_counter()
resp3 = chain.invoke({"country": "한국"})
t3 = time.perf_counter() - start
print("[SQLite] 첫 호출 응답:", resp3)
print(f"[SQLite] 첫 호출 소요 시간: {t3:.3f}초")

# 두 번째 호출 (캐시 히트 → 빠름)
start = time.perf_counter()
resp4 = chain.invoke({"country": "한국"})
t4 = time.perf_counter() - start
print("[SQLite] 두 번째 호출 응답:", resp4)
print(f"[SQLite] 두 번째 호출 소요 시간: {t4:.3f}초")