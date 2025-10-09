# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
from langchain_community.chat_message_histories import SQLChatMessageHistory

# API KEY 정보로드
load_dotenv()

# SQLChatMessageHistory 객체를 생성하고 세션 ID와 데이터베이스 연결 파일을 설정
chat_message_history = SQLChatMessageHistory(
    session_id="sql_history",
    connection="sqlite:///sqlite.db"
)

# 사용자 메시지를 추가합니다.
chat_message_history.add_user_message(
    "안녕? 만나서 반가워. 내 이름은 테디야. 나는 랭체인 개발자야. 앞으로 잘 부탁해!"
)
# AI 메시지를 추가합니다.
chat_message_history.add_ai_message("안녕 테디, 만나서 반가워. 나도 잘 부탁해!")

# 채팅 메시지 기록의 메시지들
print(chat_message_history.messages)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 1) llm 초기화
llm = ChatOpenAI(model="gpt-5-nano")

prompt = ChatPromptTemplate.from_messages(
    [
        # 시스템 메시지
        ("system", "You are a helpful assistant."),
        # 대화 기록을 위한 Placeholder
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),  # 질문
    ]
)

# chain 을 생성합니다.
chain = prompt | llm | StrOutputParser()

# 대화내용 가져오는 함수
def get_chat_history(user_id, conversation_id):
    return SQLChatMessageHistory(
        table_name=user_id,
        session_id=conversation_id,
        connection="sqlite:///sqlite.db",
    )

# config_fields 설정 (대화정보 조회 시 참고 정보 활용)
from langchain_core.runnables.utils import ConfigurableFieldSpec

config_fields = [
    ConfigurableFieldSpec(
        id="user_id",
        annotation=str,
        name="User ID",
        description="Unique identifier for a user.",
        default="",
        is_shared=True,
    ),
    ConfigurableFieldSpec(
        id="conversation_id",
        annotation=str,
        name="Conversation ID",
        description="Unique identifier for a conversation.",
        default="",
        is_shared=True,
    ),
]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,  # 대화 기록을 가져오는 함수를 설정합니다.
    input_messages_key="question",  # 입력 메시지의 키를 "question"으로 설정
    history_messages_key="chat_history",  # 대화 기록 메시지의 키를 "history"로 설정
    history_factory_config=config_fields,  # 대화 기록 조회시 참고할 파라미터를 설정합니다.
)

# config 설정
config = {"configurable": {"user_id": "user1", "conversation_id": "conversation1"}}

# 질문과 config 를 전달하여 실행합니다.
print(chain_with_history.invoke({"question": "안녕 반가워, 내 이름은 테디야"}, config))

# 후속 질문을 실행합니다.
print(chain_with_history.invoke({"question": "내 이름이 뭐라고?"}, config))

# config 설정
config = {"configurable": {"user_id": "user1", "conversation_id": "conversation2"}}

# 질문과 config 를 전달하여 실행합니다.
print(chain_with_history.invoke({"question": "내 이름이 뭐라고?"}, config))
