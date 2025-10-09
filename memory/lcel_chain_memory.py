from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

load_dotenv()

# 1) llm 초기화
llm = ChatOpenAI(model="gpt-5-nano")

# 2) prompt 구성(시스템 + 이전 대화 + 사용자 입력)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 챗봇입니다."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# 3) Memory 준비 - return_messages=True 시 HumanMessage, AIMessage 객체 반환
memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

# 4) LCEL 흐름 구성
# 먼저 memory.load_memory_variables → chat_history 꺼내고
# 그 다음 prompt → llm 순으로 연결
runnable = (
    RunnablePassthrough.assign(
        chat_history = RunnableLambda(memory.load_memory_variables)
        | (lambda d: d.get("chat_history", []))
    )
    | prompt
    | llm
)

# 5) 체인을 래핑해서 입력 처리가 끝나고 메모리에 저장되도록
def invoke_chain(user_input: str):
    result = runnable.invoke({"input": user_input})
    # 메모리에 저장 — prompt에 쓰인 입력 / 모델 출력
    memory.save_context(inputs={"human": user_input}, outputs={"ai": result.content})
    return result

# 6) 대화 시도
print(invoke_chain("안녕하세요, 반가워요!"))         # 챗봇 첫 인사
print(invoke_chain("제 이름은 김철수입니다."))      # 이름 알려주기
print(invoke_chain("제 이름이 뭐였죠?"))            # 기억한 이름 물어보기