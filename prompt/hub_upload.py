# =====================================================
# 0) 라이브러리 임포트 및 환경 변수 로딩
# =====================================================
from dotenv import load_dotenv    # .env 파일에서 환경 변수를 읽어오는 패키지
import os                         # OS 환경 변수를 다루기 위한 모듈
from langchain import hub         # LangChain Hub API를 위한 모듈

# .env 파일 내용(OPENAI_API_KEY, LANGCHAIN_API_KEY 등)을 메모리로 로드
load_dotenv()

# 환경 변수에서 API 키 꺼내기
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# 두 키가 모두 설정되어 있지 않으면 에러 발생
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
if not LANGCHAIN_API_KEY:
    raise RuntimeError("❌ LANGCHAIN_API_KEY가 설정되지 않았습니다.")


# =====================================================
# 1) 프롬프트 소유자(owner)와 레포지토리 이름 지정
# =====================================================
# Hub에 업로드할 때 사용할 "owner/prompt_name" 형식의 문자열
# owner는 LangSmith에 등록된 tenant_handle(예: 깃허브 로그인 핸들)
PROMPT_OWNER  = "cheorhyeon"
prompt_title  = "rag-prompt-korean"


# =====================================================
# 2) 프롬프트 내용 정의 (시스템·사용자 메시지)
# =====================================================
# system 메시지: 챗봇의 역할과 규칙을 설명
system = """
당신은 질문-답변(Question-Answering)을 수행하는 친절한 AI 어시스턴트입니다.
주어진 문맥(Context)에서 질문(Question)에 답하세요.
답을 모르면 '주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다'라고 답하세요.
모든 답변은 한글로 작성하되, 기술 용어나 이름은 번역하지 마세요.
"""

# human 메시지: 실제 입력 변수 자리에 질문과 문맥을 넣음
human = """
#Question: {question}

#Context: {context}
"""

from langchain.prompts import ChatPromptTemplate

# ChatPromptTemplate.from_messages:
# system 메시지와 human 메시지를 순차적으로 묶어 하나의 대화형 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", human),
    ]
)

# 템플릿 내용 확인용 출력
print("=== 정의된 Prompt 템플릿 ===")
print(prompt)


# =====================================================
# 3) Hub에 프롬프트 업로드 (push)
# =====================================================
# hub.push:
#  - 첫 번째 인자: "owner/repo" 형태의 레포 경로
#  - 두 번째 인자: 직렬화 가능한 Prompt 객체
#  - api_key: LangSmith Hub 인증용 API 키 (명시 전달)
# 기타 선택 옵션(부모 커밋, 공개 여부 등)을 추가로 지정 가능
url = hub.push(
    f"{PROMPT_OWNER}/{prompt_title}",  # 업로드 대상 경로
    prompt,                            # 위에서 만든 ChatPromptTemplate
    api_key=LANGCHAIN_API_KEY,         # Hub 인증용 키
    new_repo_is_public=True,           # True면 공개(public), False면 비공개(private)
    new_repo_description="RAG용 질문-답변 템플릿 (한글)"
)

print("✅ 업로드 완료! 확인 URL:", url)
