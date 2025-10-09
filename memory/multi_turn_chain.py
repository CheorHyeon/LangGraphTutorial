# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 Question-Answering 챗봇입니다. 주어진 질문에 대한 답변을 제공해주세요.",
        ),
        # 대화기록용 key 인 chat_history 는 가급적 변경 없이 사용하세요!
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "#Question:\n{question}"),  # 사용자 입력을 변수로 사용
    ]
)

# 1) llm 초기화
llm = ChatOpenAI(model="gpt-5-nano")

# 일반 Chain 생성
chain = prompt | llm | StrOutputParser()

# 세션 기록을 저장할 딕셔너리
store = {}

# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(abcs):
    print(f"[대화 세션ID]: {abcs}")
    if abcs not in store:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        store[abcs] = ChatMessageHistory()
    return store[abcs]  # 해당 세션 ID에 대한 세션 기록 반환

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,  # 세션 기록을 가져오는 함수
    input_messages_key="question",  # 사용자의 질문이 템플릿 변수에 들어갈 key
    history_messages_key="chat_history",  # 기록 메시지의 키
)

# ------------------------------------------
# 현재 `session_id`를 config에 넣음 / 하지만 get_session_history 매개변수는 `abcs` 임
# RunnableWithMessageHistory는 기본 모드일 때 (history_factory_config 안쓸때) 항상 `session_id` key가 필수임
# 또한 해당 history를 가져오는 함수가 단일인자일 때 매개변수가 `session_id` 든 아니든 항상 매칭됨
## 매개변수 abc 로 달라도 매칭이 됨 (sql_lite_save_conversation_by_sql_chat_message_history 에선 안됐던것)
# ------------------------------

print(
    chain_with_history.invoke(
        # 질문 입력
        {"question": "나의 이름은 테디입니다."},
        # 세션 ID 기준으로 대화를 기록합니다.
        config={"configurable": {"session_id": "abc123"}},
    )
)

print(
    chain_with_history.invoke(
        # 질문 입력
        {"question": "내 이름이 뭐라고?"},
        # 세션 ID 기준으로 대화를 기록합니다.
        config={"configurable": {"session_id": "abc123"}},
    )
)

print(
    chain_with_history.invoke(
    # 질문 입력
    {"question": "내 이름이 뭐라고?"},
    # 세션 ID 기준으로 대화를 기록합니다.
    config={"configurable": {"session_id": "abc1234"}},
    )
)
