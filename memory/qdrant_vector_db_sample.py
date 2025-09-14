import os

from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 1. Qdrant 클라이언트 연결
qdrant_client = QdrantClient(url="http://127.0.0.1:6333")

# 2. 컬렉션 생성 (없을 경우)
COLLECTION_NAME = "wikidocs_demo"
if not qdrant_client.collection_exists(COLLECTION_NAME):
    qdrant_client.create_collection(
        COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)  # 모델 출력 차원 수와 같아야 함
    )

# 3. 임베딩 모델 준비
emb = OpenAIEmbeddings(model="text-embedding-3-small",
                       api_key=OPENAI_API_KEY)

# 4. 텍스트들 임베딩해서 Qdrant에 직접 업서트
texts = [
    "파리는 에펠탑으로 유명하다.",
    "로마에는 콜로세움이 있다.",
    "취리히 근교에는 라인 폭포가 있다."
]
vectors = emb.embed_documents(texts)

# 업서트 - id를 무조건 반복문 순이라 무조건 덮어쓰도록 간단하게 구현
# 실제로는 Qdrant 순정 라이브러리 써서 ScoredPoint 객체를 얻고 거기서 id 찾아서 세팅해서 업서트 하는것이 좋을듯
qdrant_client.upsert(
    collection_name=COLLECTION_NAME,
    points=[
        {"id": i, "vector": vec, "payload": {"text": texts[i]}}
        for i, vec in enumerate(vectors)
    ]
)

# 5. LangChain Qdrant VectorStore 객체로 래핑
vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    embedding=emb,
    # Qdrant에 저장된 payload 중 하나를 골라서 Document.page_content에 넣어줌
    # 기본값은 page_content
    content_payload_key="text"
)

# 6. 텍스트 그대로 검색 (내부에서 자동 임베딩 → 유사도 검색)
query = "유럽의 유명한 폭포는?"
docs = vectorstore.similarity_search(query, k=1)
print(docs[0].page_content)