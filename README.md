## 📘 프로젝트 개요

- LangGraph 학습에 앞서 Python의 자료구조를 복습합니다.
- LangGraph 홈페이지의 `LangGraph 기본` 챕터를 무작정 따라가며 관련 개념을 간략히 학습합니다.
  - 기존 코드를 좀 더 보기 편하게 ChatGPT를 이용해서 리팩토링 및 주석을 각 단계별로 달아뒀습니다.
- LangChain, LangGraph와 관련된 여러 개념을 학습합니다.
  - 테디노트 LangChain 위키 독스를 참고하고, ChatGPT를 활용하여 PR에 해당 개념에 대한 내용을 보충합니다.
  - [출처 - 테디노트 LangChain 노트](https://wikidocs.net/book/14314)
 
-------------------------
 
## ⚙️ 실행 환경 세팅

- `.env` 파일을 생성합니다.
  - 기존 `.env.sample` 파일의 확장자를 지우고 내용을 채워둡니다.
- `Poetry` 환경을 세팅합니다.
  - PyCharm 하단에서 `Add New Interpreter`를 이용해 추가합니다.
  - 파이썬 3.12버전을 추천드립니다.
- `Poetry install`을 통해 의존성을 모두 다운 받습니다.
  - `poetry.lock` 파일은 gitIgnore에 등록되어 있지만 혹시 안된다면 커밋 시 반드시 제거해주세요

-------------------------

## 📚 사전 지식 (Prerequisite)

### Python 기초 문법

- 리스트, bool, dictionary 등 기본 자료구조 예제
  - [출처 - 점프투파이썬 위키 독스](https://wikidocs.net/book/1)
- [PR 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/4)

-------------------------

## 🚀 LangGraph 튜토리얼
- 공식 문서 `LangGraph 기본` 챕터 따라하기
- [tutorial 폴더](https://github.com/CheorHyeon/LangGraphTutorial/tree/main/tutorial)

## 💻 Prompt 학습
- LangChain의 Prompt 관련 기능 사용법 및 예제 정리
- [Prompt 폴더](https://github.com/CheorHyeon/LangGraphTutorial/tree/main/prompt)

## 🔧 Output Parser 학습
- LLM 출력 파싱·구조화 방법 
- [Output Parser 폴더](https://github.com/CheorHyeon/LangGraphTutorial/blob/main/outputParser/README.md)

## 💬 stream 방식 예시
- 에이전트 그래프 노드별 실시간 업데이트 예제
- [PR - Stream 방식 정리](https://github.com/CheorHyeon/LangGraphTutorial/pull/2)

## 🧩 Model 학습
- LangChain의 LLM 모델 설정 및 관리에 관한 내용을 다룹니다.
- OpenAI 모델 호출 최적화, 캐싱(Cache), 직렬화(Serialization) 등 예제 포함.
- [model 폴더](https://github.com/CheorHyeon/LangGraphTutorial/tree/main/model)

## 🧠 Memory 학습
- LangChain에서 대화 기억(Memory) 을 다루는 다양한 방법 실습
- 각 방식의 Deprecated 여부와 최신 권장 패턴(RunnableWithMessageHistory)을 비교 정리
- Qdrant Vector DB에 저장하고, 의미 기반 유사도 검색 수행 예제도 포함
- [memory 폴더](https://github.com/CheorHyeon/LangGraphTutorial/tree/main/memory)
