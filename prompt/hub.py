# =====================================================
# 0) 라이브러리 임포트 및 환경 변수 로딩
# =====================================================
from dotenv import load_dotenv            # .env 파일에서 환경 변수 읽기
from langchain import hub                 # LangChain Hub API
import os                                  # 운영체제 환경변수 사용

# .env 파일을 읽어 OPENAI_API_KEY, LANGCHAIN_API_KEY 설정
load_dotenv()
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# 필수 키가 없으면 에러
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
if not LANGCHAIN_API_KEY:
    raise RuntimeError("❌ LANGCHAIN_API_KEY가 설정되지 않았습니다.")


# =====================================================
# 1) Hub에서 기존 프롬프트 내려받기 (Pull)
# =====================================================
# rlm/rag-prompt 저장소의 최신 프롬프트를 가져옵니다.
prompt = hub.pull("rlm/rag-prompt")
print("=== rlm/rag-prompt 최신 버전 ===")
print(prompt)

# 특정 커밋 해시 버전을 지정해서 가져오려면 콜론(:) 뒤에 해시 추가
prompt = hub.pull("rlm/rag-prompt:50442af1")
print("=== rlm/rag-prompt@50442af1 버전 ===")
print(prompt)


# =====================================================
# 2) 새 프롬프트 정의 (ChatPromptTemplate)
# =====================================================
from langchain.prompts import ChatPromptTemplate

# ChatPromptTemplate.from_template: 간단한 템플릿에서 ChatPrompt 생성
# {context} 자리에 실제 요약할 내용을 넣도록 정의
prompt = ChatPromptTemplate.from_template(
    "주어진 내용을 바탕으로 다음 문장을 요약하세요. "
    "답변은 반드시 한글로 작성하세요.\n\n"
    "내용: {context}\n\n"
    "요약:"
)
print("=== 새로 정의한 Prompt ===")
print(prompt)


# =====================================================
# 3) Hub에 프롬프트 업로드 (Push)
# =====================================================
# hub.push:
#  - "owner/repo": 여기서는 cheorhyeon/simple-summary-korean
#  - prompt: 위에서 만든 ChatPromptTemplate 객체
#  - api_key: Hub 인증에 사용할 키
#  - new_repo_is_public: 공개 여부 (True=공개)
#  - new_repo_description: 허브 레포 설명
url = hub.push(
    "cheorhyeon/simple-summary-korean",  # tenant_handle/레포명
    prompt,
    api_key=LANGCHAIN_API_KEY,            # Hub 인증용 키
    new_repo_is_public=True,              # 공개 레포로 생성
    new_repo_description="한글 요약용 Prompt"
)

print("✅ 업로드 완료, 확인 URL:", url)
