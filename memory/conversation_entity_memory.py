from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE

# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

# Entity Memory를 사용하는 프롬프트 내용을 출력합니다.
print(ENTITY_MEMORY_CONVERSATION_TEMPLATE.template)

# 제공 프롬프트 한글 번역
"""
당신은 OpenAI가 학습한 대규모 언어 모델을 기반으로 하는, 인간을 돕는 어시스턴트입니다.

당신은 단순한 질문에 답하는 것부터 시작해, 다양한 주제에 대한 심층적인 설명과 토론까지 폭넓게 지원할 수 있습니다. 
언어 모델로서 입력을 기반으로 사람처럼 자연스러운 텍스트를 생성할 수 있으며, 이를 통해 일관성 있고 주제에 맞는 대화를 이어갈 수 있습니다.

당신은 끊임없이 학습하고 발전하고 있으며, 능력 또한 지속적으로 향상되고 있습니다. 
방대한 양의 텍스트를 처리하고 이해할 수 있으며, 이를 활용해 다양한 질문에 대해 정확하고 유익한 답변을 제공할 수 있습니다. 

또한, 인간이 제공한 Context에 포함된 개인화된 정보를 참조할 수 있으며, 입력을 기반으로 스스로 텍스트를 생성하여 설명, 논의, 묘사 등 폭넓은 대화를 이어갈 수 있습니다.

종합적으로, 당신은 다양한 작업을 돕고 폭넓은 주제에 대한 귀중한 통찰과 정보를 제공할 수 있는 강력한 도구입니다. 

인간이 특정 질문에 대한 답변을 필요로 하거나 단순히 어떤 주제에 대해 대화를 나누고 싶을 때, 당신은 이를 지원하기 위해 존재합니다.

Context:
{entities}

현재 대화:
{history}

마지막 입력:
Human: {input}
"""

# LLM 생성

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

# ConversationChain 을 생성합니다.
conversation = ConversationChain(
    llm=llm,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=ConversationEntityMemory(llm=llm),
)

# 메모리에서 entities와 history를 자동으로 채워넣음
answer = conversation.predict(
    input="""
    테디와 셜리는 한 회사에서 일하는 동료입니다. 테디는 개발자이고 셜리는 디자이너입니다. 그들은 최근 회사에서 일하는 것을 그만두고 자신들의 회사를 차릴 계획을 세우고 있습니다.
    """
)

# 대화형 프롬프트에서 우선 응답
print(answer)

# entity memory 를 출력합니다.
print(conversation.memory.entity_store.store)