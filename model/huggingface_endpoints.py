# -----------------------------------------------------
# 1) 필수 라이브러리 및 모듈 임포트
# -----------------------------------------------------
import os
from dotenv import load_dotenv                     # .env 파일에서 환경 변수 로드
from huggingface_hub import login                  # Hugging Face 허브 로그인
from langchain.prompts import PromptTemplate        # 프롬프트 템플릿 생성기
from langchain_core.output_parsers import StrOutputParser  # 문자열 출력 파서
from langchain_huggingface import HuggingFaceEndpoint     # Hugging Face Endpoint 래퍼

# -----------------------------------------------------
# 2) 환경 변수 (.env) 로드
# -----------------------------------------------------
load_dotenv()  # .env 파일의 키=값 쌍을 os.environ에 등록

# -----------------------------------------------------
# 3) Hugging Face 허브에 비대화형 로그인
# -----------------------------------------------------
#   – CLI 대화형 모드 없이 토큰만으로 인증 완료(jupiter Notobook 미사용)
login(token=os.environ["HUGGINGFACEHUB_API_TOKEN"])

# -----------------------------------------------------
# 4) 프롬프트 템플릿 정의
# -----------------------------------------------------
#   – system, user, assistant 블록으로 구성된 Chat 형식
template = """<|system|>
You are a helpful assistant.<|end|>
<|user|>
{question}<|end|>
<|assistant|>"""
prompt = PromptTemplate.from_template(template)
# prompt = PromptTemplate(
#     template=template,
#     input_variables=["question"],
# )

# -----------------------------------------------------
# 5) 사용할 모델 저장소 ID 설정
# -----------------------------------------------------
repo_id = "microsoft/Phi-3-mini-4k-instruct"

# -----------------------------------------------------
# 6) HuggingFaceEndpoint 객체 생성
# -----------------------------------------------------

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_new_tokens=256,  # max_new_tokens: 생성 길이 제한
    temperature=0.1,     # temperature: 출력 다양성 제어
    # huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],  # : 위에서 login(token) 안한 경우 엔드포인트에 넣기 가능
)

# -----------------------------------------------------
# 7) LangChain 체인 구성
# -----------------------------------------------------
chain = prompt | llm | StrOutputParser()

# -----------------------------------------------------
# 8) 체인 실행 및 결과 출력
# -----------------------------------------------------
response = chain.invoke({"question": "what is the capital of South Korea?"})
print(response)