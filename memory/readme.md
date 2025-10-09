# 🧠 memory/ 개요 (LangChain Memory 안내)
- LangChain에서 “대화/지식 기억”을 다루는 여러 방법을 작은 예제 코드로 보여줍니다.  
- 대화 기록을 어떻게 저장할지, 검색할지 등을 학습하기 위한 **참조용 코드베이스**입니다.  

---

## 1. Memory + LangChain 요약

- LangChain의 메모리 시스템은 “**이전 대화나 문맥을 기억해서 다음 프롬프트에 반영**”하는 기능을 제공합니다.
- 주요 예시:
  - `ConversationBufferMemory`
  - `VectorStoreRetrieverMemory`
  - `SQLChatMessageHistory`
  - `ChatMessageHistory`
- 최신 버전에서는 **LCEL (LangChain Expression Language)** 기반의 `RunnableWithMessageHistory`를 사용하여, 프롬프트 체인에 자동으로 기억을 주입하는 방식이 **권장**됩니다.
- 메모리 저장소는 여러 방식으로 구성할 수 있습니다:
  - 💾 **In-Memory** 저장: 속도 빠름, 휘발성  
  - 🧱 **SQL DB 저장**: 영구 저장, 다중 세션 관리 가능  
  - 🧬 **Vector DB 저장**: 임베딩 기반 검색, 의미 유사도 기반 회상  

---

## 2. `save_context()` / `load_memory_variables()` 공통 메서드 소개

LangChain의 모든 Memory 클래스가 공통으로 사용하는 핵심 메서드입니다.  
LCEL 기반으로 전환된 이후에도 기본 원리는 동일합니다.

| 메서드 | 역할 | 설명 |
|--------|------|------|
| `save_context(inputs, outputs)` | 저장 | 한 번의 대화(질문과 답변)를 메모리에 저장.<br>예: `inputs={"human": "안녕"}, outputs={"ai": "반가워요!"}` |
| `load_memory_variables(inputs)` | 불러오기 | 새로운 입력이 들어올 때, **연관된 과거 대화 기록**을 불러옴.<br>보통 `{ "history": "..." }` 형태의 딕셔너리로 반환됨 |

> 💡 LCEL 체인(`RunnableWithMessageHistory`)에서는 이 두 메서드가 내부적으로 자동 호출됩니다.

---

## 3. Deprecated된 구성 요소 & 개념적 활용

LangChain 팀은 Memory 클래스들을 LCEL 기반의 **Runnable Memory 체계**로 통합하면서  
기존 `*Memory` 계열은 “개념 학습용”으로만 남기고, 실제 사용은 중단하도록 권고했습니다.

🔗 [공식 가이드: LangChain Migration Guide – Memory](https://python.langchain.com/docs/versions/migrating_memory/)

### 주요 Deprecation 이유
- 기존 Memory 클래스는 **Chain 구성과 독립적으로 동작**하여 LCEL 파이프라인(`|`)에 통합 불가  
- **프롬프트–모델–파서 흐름** 안에서 메모리 주입이 일관되지 않음  
- 복합 상태(요약/버퍼 혼합)를 자동으로 관리하기 어려움  

### 💡 개념적 학습 포인트
> Deprecated된 Memory 클래스들도 “Agent나 RAG 구현 시 기억을 다루는 **방법론적 참고**”로는 유용합니다.

- 예: 요약형 기억, 의미 기반 검색 기억, 엔티티 중심 기억 등  
- 즉, **직접 구현용이 아니라 개념 학습용·설계 참고용**으로 이해하면 충분합니다.  

---

## 4. 주요 구성 요소 요약

| 구성 요소 | 역할 | 설명 |
|------------|------|------|
| `ChatMessageHistory` | In-Memory 기반 대화 저장 클래스 | 휘발성, 빠른 테스트용 |
| `SQLChatMessageHistory` | SQL DB 기반 대화 저장 클래스 | SQLite, PostgreSQL 등 지원 |
| `RunnableWithMessageHistory` | LCEL 체인에 메모리 주입 및 관리 담당 래퍼 | 최신 권장 구조 |
| `history_factory_config` / `ConfigurableFieldSpec` | config 값과 메모리 팩토리 함수 매핑을 명시하는 스펙 | 사용자·세션 구분용 |
| `get_session_history` / `get_chat_history` | 실제 메모리 객체(SQL 또는 In-Memory)를 반환하는 함수 | 세션별 인스턴스 관리 |
| `"prompt I llm I StrOutputParser()"` | LCEL 기반 프롬프트 → LLM → 결과 변환 기본 체인 구조 | 표준 파이프라인 구성 |

* `prompt I llm I StrOutputParser()` 에서 `I`는 `|` 기호 대체 (마크다운 표 인식 이슈)
---

## 5. 구현 정보

| 제목 | 주요 내용 | 비고 | PR |
|------|-----------|------|----|
| **대화 버퍼 메모리 (ConversationBufferMemory)** | 간단 대화 기록 저장했다가 그대로 불러오는 가장 기본적 메모리 방식 | ⚠️ **Deprecated** | [PR #21 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/21) |
| **대화 버퍼 윈도우 메모리 (ConversationBufferWindowMemory)** | 모든 대화 내용이 아닌 최근 K개 대화 기록만 불러옴 | ⚠️ **Deprecated** | [PR #22 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/22) |
| **대화 토큰 버퍼 메모리 (ConversationTokenBufferMemory)** | 최근 대화를 **토큰 길이 기준**으로 관리하는 버퍼 메모리 | ⚠️ **Deprecated** | [PR #23 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/23) |
| **대화 엔티티 메모리 (ConversationEntityMemory)** | 대화 중 등장한 **고유명사(엔티티)**를 추출·요약하여 모델이 기억한 듯 응답하도록 구성 | ⚠️ **Deprecated** | [PR #24 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/24) |
| **대화 지식 그래프 메모리 (ConversationKGMemory)** | 대화를 **지식 그래프(개체·관계)** 형태로 구조화해 기억 | ⚠️ **Deprecated** | [PR #25 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/25) |
| **대화 요약 메모리 (ConversationSummaryMemory)**<br>**+ ConversationSummaryBufferMemory** | 대화를 요약하며, 긴 대화에서는 과거는 요약·최근은 원문(버퍼)으로 유지하는 하이브리드 방식 | ⚠️ **Deprecated** | [PR #26 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/26) |
| **Qdrant 임베딩하여 저장 및 유사도 검색 예시** | 텍스트를 OpenAI 임베딩 모델로 벡터화해 Qdrant Vector DB에 저장하고, 의미 기반 유사도 검색 수행 예제 | 🔰 Qdrant 기본 실습 (Vector DB 개념 학습용) | [PR #27 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/27) |
| **벡터저장소 검색 메모리 (VectorStoreRetrieverMemory)** | 대화나 지식을 **벡터DB에 임베딩** 저장 후, 의미적으로 유사한 기록을 검색 | ⚠️ **Deprecated** | [PR #28 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/28) |
| **LCEL 체인에 메모리 추가** | **LangChain Expression Language (LCEL)**을 사용해 프롬프트–LLM–메모리를 직접 연결<br>기존 Memory 클래스를 완전히 대체하는 구조 | ✅ **최신 권장 방식** | [PR #29 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/29) |
| **SQLChatMessageHistory + RunnableWithMessageHistory** | `SQLChatMessageHistory`로 대화 이력을 **SQLite DB에 영구 저장**<br>`RunnableWithMessageHistory`를 통해 세션별 히스토리 자동 관리 | ✅ **최신 권장 방식** | [PR #30 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/30) |
| **RunnableWithMessageHistory + ChatMessageHistory** | 인메모리 딕셔너리(`store`) 기반 세션 관리 예제. `session_id`별로 대화 내역을 분리 저장 | ✅ **최신 권장 방식** | [PR #31 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/31) |

---

## 📚 학습 가이드 요약

| 구분 | 학습 난이도 | 권장 학습 방향 |
|------|--------------|----------------|
| ⚠️ Deprecated 계열 | ⭐⭐ | Memory 구조 개념 이해용. 실제 구현보다는 설계 아이디어 참고. |
| ✅ 최신 권장 계열 | ⭐⭐⭐⭐ | 실무 및 프로젝트 적용 가능. LCEL + Runnable 구조 필수 학습 대상. |

---

> 🧩 LangChain의 Memory 시스템은  
> `Conversation*Memory` → `RunnableWithMessageHistory`로 완전히 진화했습니다.  
> LCEL 기반으로 체인 안에서 메모리를 통합 관리하는 것이 이제 표준이며,  
> Deprecated된 클래스들은 “개념 학습용”으로만 참고하면 충분하다고 합니다!
