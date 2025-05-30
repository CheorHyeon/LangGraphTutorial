# 개요
- LangGraph 홈페이지의 `LangGraph 기본` 챕터를 무작정 따라가며 관련 개념을 간략히 학습합니다.
  - 기존 코드를 좀 더 보기 편하게 ChatGPT를 이용해서 리팩토링 및 주석을 각 단계별로 달아뒀습니다.
  - 기존 홈페이지 예시와 다르게 LLM을 ChatGPT OpenAI-4o-mini 모델을 이용합니다.
  - 기존 홈페이지의 가이드 LangGraph 기본 부분을 학습했습니다.
    - [LangGraph 기본 - 개요](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/)
    - 사이트 구성이 변경되어 PR 단위가 맞지 않을 수 있습니다.

-----------------------

## 1부 : 기본 챗봇 만들기
- `BaseMessage 객체`로 자동 생성되는 내용을 본문에서 다룹니다.
- [1부 완성 PR 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/1)

## 2부 : 도구 추가
- `add_conditional_edges` 문법에 대해 다루며, 조건만 검사하는 별도 노드를 생성하지 않아도 동작함을 정리했습니다.
- Python의 Class에 대한 문법을 정리했습니다.
  - `__call__` 메서드를 정의하면 인스턴스의 이름을 함수로 사용할 수 있는 문법을 정리했습니다.
- [2부 완성 PR 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/3)

## 3부 : 메모리 추가
- 현재까지 구현한 챗봇은 이전 상호작용의 맥락을 기억하지 못해 일관성 있고 여러 차례 대화가 이어지는 대화가 제한됩니다.
- LangGraph는 checkpointer 그래프를 컴파일때 제공하여 문제 해결
  - 그래프를 컴파일할때 checkpointer=000 옵션을 주면 LangGraph가 각 노드 실행 후 상태를 자동 저장
- [3부 완성 PR 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/5)

## 4부 : Human-in-the-Loop
- 일부 작업의 경우 모든 것이 의도한 대로 실행되는지 확인하기 위해 실행 전에 사람의 승인을 받아야 할 수도 있습니다.
- 사용자 참여형 (Human-in-the-Loop) 워크플로를 지원하여 사용자 피드백에 따라 실행을 일시 중지하고 재개할 수 있습니다.
- [4부 완성 PR 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/6)

## 5부 : Customizing State
- 메시지 목록에 의존하지 않고 복잡한 동작을 정의하기 위해 상태에 필드를 추가합니다.
- 프롬프트 지시 사항과 맞지 않아 도구를 사용 하지 않아야 하는게 맞지 않나? 라는 의문을 가졌으나 이와 관련한 내용을 정리했습니다.
- [5부 완성 PR 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/7)

## 6부 : 시간여행(Time travel)
- 사용자가 이전 응답에서 시작해 별도 결과를 탐색 or 사용자가 어시스턴트의 작업을 되돌려 오류 수정 or 다른 전략 시도
- 그래프의 메서드를 이용하여 체크 포인트를 가져온 뒤 그래프를 되감는 예제
- get_state_history 메서드에 대해서도 설명을 추가했습니다.
- [6부 완성 PR 바로가기](https://github.com/CheorHyeon/LangGraphTutorial/pull/8)
