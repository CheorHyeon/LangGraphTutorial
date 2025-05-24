#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =====================================================
# 1) 환경 설정 로드 & API 키 검증
# =====================================================
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다.")

# =====================================================
# 2) LangChain LLM 초기화
# =====================================================
from langchain_openai import ChatOpenAI

# gpt-4.1-mini 모델 사용
llm = ChatOpenAI(model="gpt-4.1-mini")

# =====================================================
# 3) 프롬프트 & 체인 생성
# =====================================================
from langchain_core.prompts import PromptTemplate

# "{fruit}의 색상이 무엇입니까?" 라는 질문 템플릿
prompt = PromptTemplate(
    template="{fruit}의 색상이 무엇입니까?",
    input_variables=["fruit"]
)

# 템플릿 + LLM을 연결해 '체인' 생성
chain = prompt | llm

# =====================================================
# 4) 직렬화 가능 여부 확인
# =====================================================
# 클래스, 인스턴스, 체인이 모두 직렬화 지원하는지 체크
print("LLM 클래스 직렬화 가능:", ChatOpenAI.is_lc_serializable())
print("LLM 인스턴스 직렬화 가능:", llm.is_lc_serializable())
print("체인 직렬화 가능:", chain.is_lc_serializable())

# =====================================================
# 5) 체인 직렬화: dict & JSON 문자열
# =====================================================
from langchain_core.load import dumpd, dumps

# dumpd → 파이썬 dict로 직렬화
serialized_dict = dumpd(chain)
print("직렬화된 dict:", serialized_dict, type(serialized_dict))

# dumps → JSON 문자열로 직렬화
serialized_json = dumps(chain)
print("직렬화된 JSON 문자열:", serialized_json[:100], "...", type(serialized_json))

# =====================================================
# 6) 직렬화 데이터 저장 & 로드
# =====================================================
import pickle
import json

# ---- 6.1) pickle 포맷으로 저장 (바이너리) ----
with open("fruit_chain.pkl", "wb") as f1:
    pickle.dump(serialized_dict, f1)
# 파일이 자동으로 닫히므로 f.close() 생략 가능

# ---- 6.2) JSON 포맷으로 저장 (텍스트) ----
with open("fruit_chain.json", "w", encoding="utf-8") as f2:
    # ensure_ascii=False 로 한글이 깨지지 않게, indent=2 로 보기 좋게 저장
    json.dump(serialized_dict, f2, ensure_ascii=False, indent=2)

# =====================================================
# 7) 저장된 데이터로 체인 복원 & 실행
# =====================================================
from langchain_core.load import load, loads

# ---- 7.1) pickle에서 로드 후 복원 ----
with open("fruit_chain.pkl", "rb") as f3:
    loaded_dict = pickle.load(f3)

# pickle 매핑 단계에서 secret도 같이 직렬화 되어 복구하면 그대로 사용 가능
restored_chain_pickle = load(loaded_dict)
print("Pickle 복원 체인 실행 결과:",
      restored_chain_pickle.invoke({"fruit": "사과"}))

# ---- 7.2) JSON에서 로드 후 복원 (UTF-8 명시)----
with open("fruit_chain.json", "r", encoding="utf-8") as f4:
    loaded_json = json.load(f4)

restored_chain_json = load(
    loaded_json,
    secrets_map={"OPENAI_API_KEY": OPENAI_API_KEY}
)

print("JSON 복원 체인 실행 결과:",
      restored_chain_json.invoke({"fruit": "사과"}))
