# 개요
- 테디노트 랭그래프 부분에서 출력 파서 부분을 정리합니다.
- 위키독스에 나와 있는 예시를 사용하지 않고 Chat GPT를 통해 예시를 만들고 사용합니다.
  - 일부 개념은 인용해서 학습하고 정리하고자 합니다.
- [출처 - 테디노트 위키독스 출력 파서 부분](https://wikidocs.net/233771)
- 환경 변수 설정은 레포지토리 메인 페이지의 Readme 파일을 참조하세요.

## 출력 파서(Output parser)

- 언어 모델(LLM)의 출력을 더 유용하고 구조화된 형태로 변환하는 중요한 컴포넌트
- 다양한 종류의 출력 데이터 파싱 및 처리
- LLM 출력을 보다 효과적 활용, 구조화된 데이터 쉽게 변환

## 이점

- 구조화 : LLM의 자유 형식 텍스트 출력을 구조화된 데이터 변환
- 일관성 : 출력 형식 일관 유지, 후속 처리 용이
- 유연성 : 다양한 출력 형식(JSON, 리스트, 딕셔너리 등) 변환 가능

## 작성한 파서 종류

- PydanticOutputParser
  - 언어 모델의 출력을 더 구조화된 정보로 변환하는데 도움이 되는 클래스 
  - [PydanticOutputParser](https://github.com/CheorHyeon/LangGraphTutorial/pull/9)
- CommonSeparatedListOutputParser
  - 쉼표로 구분된 항목 목록 반환 필요가 있을때 유용
  - [CommaSeparatedListOutputParser](https://github.com/CheorHyeon/LangGraphTutorial/pull/11)
- RegexParser
  - 모르고 main 브랜치에 바로 커밋하여 아래 설명 작성.. 
    - [feat : RegexParser_v1 완성](https://github.com/CheorHyeon/LangGraphTutorial/commit/c9f7042b254b41abf3270e966ab3d1f1be70f50e)
    - [feat : RegexParser_v2 완성](https://github.com/CheorHyeon/LangGraphTutorial/commit/8659d9764cca6dd5f6876839e093c31ee4ce5416)
  - 정규표현식(Regex)으로 텍스트에서 캡처 그룹을 뽑아 지정한 `output_keys` 순서대로 `dict` 로 반환
	- `Key: Value` 형태나 고정된 포맷에서 일부 정보만 뽑아낼 때 자주 사용됨

  - 파서 초기화
```python
parser = RegexParser(  
    # 추출할 패턴을 담은 정규표현식  
    ## 명명된 캡처 그룹 (` (?P<name>...) `) 또는 위치 기반 그룹 ( `(...)` ) 사용 가능  
    regex=r"Name:\s*(?P<name>\w+),\s*Age:\s*(?P<age>\d+)",  
    
    # 캡처된 그룹을 어떤 키로 반환할지 순서대로 지정  
    ## 명명된 그룹을 쓸 때는 그룹 이름과 겹치지 않아도 되지만 순서를 맞춰 주면 안전  
    output_keys=["name", "age"],  
    
    # (선택) 패턴 매칭에 실패했을 때 반환할 기본 키 -> 보통 None으로 두어 매칭 실패 시 빈 dict 
    default_output_key = None  
)
```

- default_output_key 옵션 관련

```python

# default_output_key=None (매칭 실패 → {})
parser_none = RegexParser(regex=your_regex, output_keys=["a","b"], default_output_key=None)
print(parser_none.parse("not match"))  # {}

# default_output_key="fallback" (매칭 실패 → {"fallback": "not match"})
parser_fb = RegexParser(regex=your_regex, output_keys=["a","b"], default_output_key="fallback")
print(parser_fb.parse("not match"))    # {'fallback': 'not match'}

```

---

## 파서별 특징 요약

- LangChain의 기본 제공 OutputParser들은 2가지 파서로 나뉨
  - 프롬프트에 자동으로 "이런 형식으로 응답해달라" 라는 지침을 생성하는 파서
    - JSON, XML, CSV, StructuredOutputParser처럼 복잡한 스키마 다룰때 유용
    - `get_format_instructions()` 메서드를 통해 자동으로 포맷 지침 생성
  - 단순 후처리용 파서
    - RegexParser, CommaSeparatedListOutputParser, ListOutputParser 등
    - LLM의 응답을 단순히 파싱만 하기에 별도 자동 지침 생성 기능 없음
      - 프롬프트에 직접 "쉼표로 구분해 주세요" 같은 명시적 지시 넣어야 함

### `get_format_instructions()` 지원 유무와 기능을 한눈에 정리한 표


| 파서 이름                             | `get_format_instructions()` 지원 여부 | 주요 기능                                           |
|--------------------------------------|--------------------------------------|----------------------------------------------------|
| **StrOutputParser**                  | 아니요                               | 메시지나 문자열에서 최상위 텍스트를 추출 (`str`) |
| **JsonOutputParser**                 | 예                                   | LLM 응답을 JSON 객체로 파싱 (Pydantic 모델 지원)   |
| **SimpleJsonOutputParser**           | 예                                   | `JsonOutputParser`의 별칭, 동일하게 JSON 파싱      |
| **CommaSeparatedListOutputParser**   | 아니요                               | 쉼표로 구분된 문자열을 `List[str]`로 변환           |
| **ListOutputParser**                 | 아니요                               | LLM 응답을 줄 단위 리스트로 파싱 (`List[str]`)     |
| **MarkdownListOutputParser**         | 아니요                               | 마크다운 리스트(`- item` 등)를 `List[str]`로 파싱  |
| **NumberedListOutputParser**         | 아니요                               | 번호 매겨진 리스트(`1. item`)를 `List[str]`로 파싱 |
| **RegexParser**                      | 아니요                               | 정규표현식으로 텍스트에서 그룹별 값을 뽑아 `dict` 반환 |
| **XMLOutputParser**                  | 예                                   | XML 형태 응답을 `dict`로 파싱                     |
| **CsvOutputParser**                  | 예                                   | 쉼표 구분 CSV 문자열을 `List[str]`로 파싱          |
| **PydanticOutputParser**             | 아니요*                              | Pydantic 모델에 맞춰 JSON 응답을 검증·파싱 (invoke() 사용) |
| **YamlOutputParser**                 | 아니요                               | YAML 블록을 Pydantic 모델로 파싱                   |
| **EnumOutputParser**                 | 아니요                               | 지정한 `Enum` 값 중 하나로 매핑                    |
| **DatetimeOutputParser**             | 예                                   | 날짜/시간 문자열을 `datetime` 객체로 파싱         |
| **StructuredOutputParser**           | 예                                   | `ResponseSchema` 기반으로 문자열을 `Dict[str,Any]`로 파싱 |
| **OutputFixingParser**               | 아니요                               | 다른 파서를 래핑하여, 에러 시 LLM을 호출해 출력 수정 |
| **RetryWithErrorParser**             | 아니요                               | 파싱 실패 시 LLM에 원본과 에러를 보내 재시도하도록 요청 |
