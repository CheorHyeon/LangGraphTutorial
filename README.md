## 📘 프로젝트 개요

- LangGraph 학습에 앞서 Python의 자료구조를 복습합니다.
- LangGraph 홈페이지의 `LangGraph 기본` 챕터를 무작정 따라가며 관련 개념을 간략히 학습합니다.
  - 기존 코드를 좀 더 보기 편하게 ChatGPT를 이용해서 리팩토링 및 주석을 각 단계별로 달아뒀습니다.
- LangGraph와 관련된 여러 개념을 학습합니다.
  - Output Parser 관련 학습
  - stream 방식 관련 학습
 
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

## 🔧 Output Parser 학습
- LLM 출력 파싱·구조화 방법 
- [Output Parser 폴더](https://github.com/CheorHyeon/LangGraphTutorial/blob/main/outputParser/README.md)

## 💬 stream 방식 예시
- 에이전트 그래프 노드별 실시간 업데이트 예제
- [PR - Stream 방식 정리](https://github.com/CheorHyeon/LangGraphTutorial/pull/2)

## 💻 Prompt 학습
- LangChain의 Prompt 관련 기능 사용법 및 예제 정리
- [Prompt 폴더](https://github.com/CheorHyeon/LangGraphTutorial/tree/main/prompt)
