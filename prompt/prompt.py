# =====================================================
# 0) 환경 변수 로딩
# =====================================================
# .env 파일에 OPENAI_API_KEY를 저장해 두었다면 여기서 불러옵니다.
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# =====================================================
# 1) LLM 객체 생성
# =====================================================
# langchain_openai 패키지의 ChatOpenAI를 사용해 LLM 인스턴스를 만듭니다.
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# =====================================================
# 2) PromptTemplate 기본 사용법
# =====================================================
from langchain_core.prompts import PromptTemplate

# 방법 1: from_template() 으로 간단 생성
template = "{country}의 수도는 어디인가요?"
prompt1 = PromptTemplate.from_template(template)
print(prompt1)

# 체인으로 묶어서 직접 invoke 하기
chain1 = prompt1 | llm
out1 = chain1.invoke("대한민국").content
print(out1)  # "대한민국의 수도는 서울입니다."

# =====================================================
# 3) PromptTemplate 생성자 사용 + .format()
# =====================================================
# input_variables를 명시하면 해당 변수 누락 시 에러
prompt2 = PromptTemplate(
    template="{country}의 수도는 어디인가요?",
    input_variables=["country"],
)

# .format() / .invoke() 메서드로 프롬프트를 생성할 수 있다.
text2 = prompt2.format(country="프랑스")
text3 = prompt2.invoke({"country":"프랑스"})
print(text2)  # "프랑스의 수도는 어디인가요?"
print(text3)  # text='프랑스의 수도는 어디인가요?'
print(text3.text) #  프랑스의 수도는 어디인가요?

# =====================================================
# 4) partial_variables 활용
# =====================================================
import datetime

# 오늘 날짜 추출
def get_today():
    return datetime.datetime.now().strftime("%B %d")

# today 변수는 매번 자동 갱신되는 partial 변수로 설정
prompt3 = PromptTemplate(
    template="오늘은 {today} 입니다. {n}개의 동물을 나열해 주세요.",
    input_variables=["n"],
    # 프롬프트 템플릿에 삽입되는 변하는 값이나 사용자의 입력을 받는 것이 아닌 고정된 값 지정할 수 있음
    partial_variables={"today": get_today},
)
chain3 = prompt3 | llm
out3 = chain3.invoke({"n": 5}).content
print(out3)

# =====================================================
# 5) 다중 변수 + partial 변경
# =====================================================
# country1은 매번 외부에서, country2는 기본값으로 '미국'
template_multi = "{country1}과 {country2}의 수도는?"
prompt4 = PromptTemplate(
    template=template_multi,
    input_variables=["country1"],
    partial_variables={"country2": "미국"},
)
chain4 = prompt4 | llm
# country2는 partial_variables로 기본값이 지정되어 있어 기본값이 적용된다.
out4 = chain4.invoke({"country1": "대한민국"}).content
print(out4)  # "대한민국의 수도는 서울이고, 미국의 수도는 워싱턴 D.C.입니다."

# country2는 partial_variables로 기본값이 지정되어 있지만, 체인 실행 시 지정하면 해당 값이 우선 적용된다.
out4 = chain4.invoke({"country1": "대한민국", "country2": "일본"}).content
print(out4)  # "대한민국의 수도는 서울이고, 일본의 수도는 도쿄입니다."

# 프롬프트를 채우고 llm에 직접 텍스트가 채워진 프롬프트를 넘겨서 실행해도 결과는 동일하다.
prompt4_1 = prompt4.invoke({"country1": "대한민국", "country2": "일본"})
out4_1 = llm.invoke(prompt4_1).content
print(out4_1)  # "대한민국의 수도는 서울이고, 일본의 수도는 도쿄입니다."

# =====================================================
# 6) 파일로부터 Prompt 불러오기 (YAML)
# =====================================================
from langchain_core.prompts import load_prompt

from pathlib import Path

# prompt.py가 위치한 폴더를 작업 디렉터리로 변경
os.chdir(Path(__file__).parent)

try:
    prompt_file = load_prompt("fruit_color.yaml", encoding="utf-8")
    chain5 = prompt_file | llm
    out5 = chain5.invoke({"fruit": "바나나"}).content
    print(out5)  # "바나나의 색깔은 노란색입니다."
except FileNotFoundError:
    print("fruit_color.yaml 파일을 찾을 수 없어 예제를 건너뜁니다.")

# =====================================================
# 7-1) ChatPromptTemplate 사용 예시 1
# =====================================================
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages(
	[
		# role, message 튜플 형태
		("system", "당신은 친절한 AI 어시스턴트입니다. 당신의 이름은 {name} 입니다."),
		("human", "반가워요!"),
		("ai", "안녕하세요! 무엇을 도와드릴까요?"),
		("human", "{user_input}"),
	]
)

# 챗 message 를 생성합니다.
messages = chat_template.format_messages(
	name="테디",
	user_input="당신의 이름은 무엇입니까?"
)

# 대화 목록 완성
print(messages)

# 추출한 메시지를 바로 LLM에 주입하여 결과를 얻을 수 있습니다.
print(llm.invoke(messages).content)

# =====================================================
# 7-2) ChatPromptTemplate 사용 예시 2
# =====================================================
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage

# system 메시지 + 대화(history) + human 메시지 예시
chat_tpl = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 친절한 AI 어시스턴트입니다."),
        # 어떤 역할을 사용할지 불확실 or 서식 지정 중 메시지 목록을 삽입할 경우
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_input}")
    ]
)

# dict로 바로 넘기는 방식
chain7 = chat_tpl | llm
out_chat = chain7.invoke(
    {
        "history": [
            SystemMessage(content="처음 인사"),
            HumanMessage(content="안녕하세요!")
        ],
        "user_input": "오늘 날씨 어때?"
    }
).content
print(out_chat)