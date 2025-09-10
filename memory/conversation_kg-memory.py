# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationKGMemory

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

memory = ConversationKGMemory(llm=llm, return_messages=True)
# LLM 호출하여 엔티티 / 관계 추출
memory.save_context(
    {"input": "이쪽은 Pangyo 에 거주중인 김셜리씨 입니다."},
    {"output": "김셜리씨는 누구시죠?"},
)
memory.save_context(
    {"input": "김셜리씨는 우리 회사의 신입 디자이너입니다."},
    {"output": "만나서 반갑습니다."},
)

# 엔티티 1회 호출 : - 현재 input 속 엔티티를 뽑고, 그 엔티티와 관련된 지식 그래프 내용 요약해서 반환
print(memory.load_memory_variables({"input": "김셜리씨는 누구입니까?"}));