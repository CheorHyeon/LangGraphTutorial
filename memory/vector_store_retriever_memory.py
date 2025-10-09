# Qdrant + VectorStoreRetrieverMemory 버전
import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.memory import VectorStoreRetrieverMemory
# API KEY 정보로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 임베딩 모델을 정의합니다.
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small",
                       api_key=OPENAI_API_KEY)

# 2) Qdrant 클라이언트 + 컬렉션 (없으면 생성)
COLLECTION = "interview_memory"
client = QdrantClient(url="http://127.0.0.1:6333")

if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),  # 모델 차원과 일치!
    )

# 3) LangChain용 VectorStore 래핑
# payload의 본문 키를 page_content로 쓸 것이므로 content_payload_key="page_content"
vectorstore = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION,
    embedding=embeddings_model,
    content_payload_key="page_content",
)

# 4) Retriever & Memory (질의와 가장 유사한 1건만)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
memory = VectorStoreRetrieverMemory(
    retriever=retriever,
    memory_key="history",  # load_memory_variables에서 가장 유사한 대화 내용이 반환될 키 지정
)

# 임의의 대화를 저장합니다.
memory.save_context(
    inputs={
        "human": "안녕하세요, 오늘 면접에 참석해주셔서 감사합니다. 자기소개 부탁드립니다."
    },
    outputs={
        "ai": "안녕하세요. 저는 컴퓨터 과학을 전공한 신입 개발자입니다. 대학에서는 주로 자바와 파이썬을 사용했으며, 최근에는 웹 개발 프로젝트에 참여하여 실제 사용자를 위한 서비스를 개발하는 경험을 했습니다."
    },
)
memory.save_context(
    inputs={"human": "프로젝트에서 어떤 역할을 맡았나요?"},
    outputs={
        "ai": "제가 맡은 역할은 백엔드 개발자였습니다. 사용자 데이터 처리와 서버 로직 개발을 담당했으며, RESTful API를 구현하여 프론트엔드와의 통신을 담당했습니다. 또한, 데이터베이스 설계에도 참여했습니다."
    },
)
memory.save_context(
    inputs={
        "human": "팀 프로젝트에서 어려움을 겪었던 경험이 있다면 어떻게 해결했나요?"
    },
    outputs={
        "ai": "프로젝트 초기에 의사소통 문제로 몇 가지 어려움이 있었습니다. 이를 해결하기 위해 저희 팀은 정기적인 미팅을 갖고 각자의 진행 상황을 공유했습니다. 또한, 문제가 발생했을 때는 적극적으로 의견을 나누고, 합리적인 해결책을 찾기 위해 노력했습니다."
    },
)
memory.save_context(
    inputs={"human": "개발자로서 자신의 강점은 무엇이라고 생각하나요?"},
    outputs={
        "ai": "제 강점은 빠른 학습 능력과 문제 해결 능력입니다. 새로운 기술이나 도구를 빠르게 습득할 수 있으며, 복잡한 문제에 직면했을 때 창의적인 해결책을 제시할 수 있습니다. 또한, 팀워크를 중시하며 동료들과 협력하는 것을 중요하게 생각합니다."
    },
)

memory_variables = memory.load_memory_variables({"prompt": "면접자 전공은 무엇인가요?"})

# 메모리에 질문을 통해 가장 연관성 높은 1개 대화를 추출합니다.
print(memory.load_memory_variables({"prompt": "면접자 전공은 무엇인가요?"})["history"])

