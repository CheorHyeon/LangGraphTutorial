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
  - [Common separeted list output parser](https://github.com/CheorHyeon/LangGraphTutorial/pull/11)
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
