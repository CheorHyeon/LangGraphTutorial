# 📄 출력 파서 정리

## 1. 개요
- 언어 모델(LLM)의 출력 결과를 **유용하고 구조화된 형태**로 바꾸는 컴포넌트입니다.  
- 위키독스 예시 대신 **ChatGPT**로 직접 만들어본 예시들을 활용해 학습·정리했습니다.
  - [출처: 테디노트 위키독스 출력 파서](https://wikidocs.net/233771)  
- 환경 변수 설정 등은 메인 README를 참고하세요.

## 2. 출력 파서(Output parser)란?

- 언어 모델(LLM)의 출력을 더 유용하고 구조화된 형태로 변환하는 중요한 컴포넌트
- 다양한 종류의 출력 데이터 파싱 및 처리
- LLM 출력을 보다 효과적 활용, 구조화된 데이터 쉽게 변환

## 3. 이점

- 구조화 : LLM의 자유 형식 텍스트 출력을 구조화된 데이터 변환
- 일관성 : 출력 형식 일관 유지, 후속 처리 용이
- 유연성 : 다양한 출력 형식(JSON, 리스트, 딕셔너리 등) 변환 가능

## 4. 구현한 파서 종류

| 파서 이름                             | 용도                                                    | 링크                                                         |
|:--------------------------------------|:--------------------------------------------------------|:-------------------------------------------------------------|
| **PydanticOutputParser**              | Pydantic 모델 기반 JSON 지침 생성 & 인스턴스 반환       | [PydanticOutputParser](https://github.com/CheorHyeon/LangGraphTutorial/pull/9)   |
| **CommaSeparatedListOutputParser**    | 쉼표로 구분된 문자열 → `List[str]` 변환                  | [CommaSeparatedListOutputParser](https://github.com/CheorHyeon/LangGraphTutorial/pull/11) |
| **RegexParser**                       | 정규식 캡처 그룹 → `dict` 반환                           | 하단 설명에 링크 포 |
                 
### 4.1. RegexParser 
- main 브랜치에 바로 커밋하여 아래 설명 작성
  - [feat : RegexParser_v1 완성](https://github.com/CheorHyeon/LangGraphTutorial/commit/c9f7042b254b41abf3270e966ab3d1f1be70f50e)
  - [feat : RegexParser_v2 완성](https://github.com/CheorHyeon/LangGraphTutorial/commit/8659d9764cca6dd5f6876839e093c31ee4ce5416)

- 정규표현식(Regex)으로 텍스트에서 캡처 그룹을 뽑아 지정한 `output_keys` 순서대로 `dict` 로 반환
  - `Key: Value` 형태나 고정된 포맷에서 일부 정보만 뽑아낼 때 자주 사용

- RegexParser 사용 예시
  
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

## 5. 파서 분류 및 특징
- 포맷 지침 생성 파서와 단순 후처리 파서 두 종류로 나뉨

### 5-1. 포맷 지침 생성 파서

- **자동 지침 생성** : 파서 객체를 생성할 때(Pydantic 모델·ResponseSchema 등 스키마 기반) 내부에서 “응답 형식” 지침(format instructions)을 미리 생성해 두고, `get_format_instructions()` 호출 시 이를 반환
  - 응답 형식 : LLM에게 `응답은 아래와 같은 JSON 형태로 해줘` 라는 식의 응답 출력 형식 지정하는 것
  - ex) PydanticOutputParser의 PydanticModel로 인해 자동으로 생성되는 응답 형식

```python
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:

{
  "properties": {
    "setup": {
      "description": "농담의 질문 부분", 
      "title": "Setup", 
      "type": "string"
     }, 
    "punchline": {
      "description": "농담의 답변 부분", 
      "title": "Punchline", 
      "type": "string"
     }
  }, 
  "required": ["setup", "punchline"]
}
```

- **용도**
  - LLM에게 `이런 형태로 응답해 주세요`를 강제할 때  
  - 스키마 검증이 필요한 경우

- **대표 파서**:  
  - `PydanticOutputParser`  
  - `StructuredOutputParser`  
  - `DatetimeOutputParser`  
  - `XmlOutputParser`  
  - `CsvOutputParser`  

### 5-2. 단순 후처리 파서

- **자동 지침 없음** : 파서 생성 시 별도의 format-instructions를 만들지 않으므로, `쉼표로 나눠 주세요`, `정규식으로 뽑아 주세요` 와같은 `응답 형식지시`는 **프롬프트에 직접** 작성해야 함

- **용도**:  
  - LLM의 자유 텍스트를 간단히 리스트, 딕셔너리, Boolean 등으로 변환할 때  
  - 별도의 스키마 검증이 필요 없을 때

- **대표 파서**:  
  - `CommaSeparatedListOutputParser`  
  - `ListOutputParser` / `MarkdownListOutputParser` / `NumberedListOutputParser`  
  - `RegexParser`  
  - `EnumOutputParser`  
  - `OutputFixingParser` / `RetryWithErrorParser`  

### `get_format_instructions()` 지원 유무와 기능을 한눈에 정리한 표


| 파서 이름                             | `get_format_instructions()` 지원 여부 | 주요 기능                                           |
|:--------------------------------------:|:--------------------------------------:|:----------------------------------------------------:|
| **StrOutputParser**                  |❌                               | 메시지나 문자열에서 최상위 텍스트를 추출 (`str`) |
| **JsonOutputParser**                 |✅                                   | LLM 응답을 JSON 객체로 파싱 (Pydantic 모델 지원)   |
| **SimpleJsonOutputParser**           |✅                                   | `JsonOutputParser`의 별칭, 동일하게 JSON 파싱      |
| **CommaSeparatedListOutputParser**   |❌                              | 쉼표로 구분된 문자열을 `List[str]`로 변환           |
| **ListOutputParser**                 |❌                               | LLM 응답을 줄 단위 리스트로 파싱 (`List[str]`)     |
| **MarkdownListOutputParser**         |❌                              | 마크다운 리스트(`- item` 등)를 `List[str]`로 파싱  |
| **NumberedListOutputParser**         |❌                              | 번호 매겨진 리스트(`1. item`)를 `List[str]`로 파싱 |
| **RegexParser**                      |❌                              | 정규표현식으로 텍스트에서 그룹별 값을 뽑아 `dict` 반환 |
| **XMLOutputParser**                  |✅                                   | XML 형태 응답을 `dict`로 파싱                     |
| **CsvOutputParser**                  |✅                                   | 쉼표 구분 CSV 문자열을 `List[str]`로 파싱          |
| **PydanticOutputParser**             |✅                            | Pydantic 모델 스키마 기반 JSON 지침 생성 및 `invoke()`로 모델 인스턴스 반환 |
| **YamlOutputParser**                 |❌                              | YAML 블록을 Pydantic 모델로 파싱                   |
| **EnumOutputParser**                 |❌                               | 지정한 `Enum` 값 중 하나로 매핑                    |
| **DatetimeOutputParser**             |✅                                   | 날짜/시간 문자열을 `datetime` 객체로 파싱         |
| **StructuredOutputParser**           |✅                                   | `ResponseSchema` 기반으로 문자열을 `Dict[str,Any]`로 파싱 |
| **OutputFixingParser**               |❌                               | 다른 파서를 래핑하여, 에러 시 LLM을 호출해 출력 수정 |
| **RetryWithErrorParser**             |❌                               | 파싱 실패 시 LLM에 원본과 에러를 보내 재시도하도록 요청 |
