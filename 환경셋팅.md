# 실습 환경 셋팅 가이드

## 환경 정보
- OS: Windows 11
- Shell: PowerShell
- 패키지 관리: uv
- LLM API: OpenAI API

---

## 1. uv 설치

PowerShell을 **관리자 권한**으로 실행 후 아래 명령어를 실행합니다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

설치 확인:

```powershell
uv --version
```

---

## 2. 프로젝트 폴더 이동

```powershell
mkdir langgraph_modular_rag
cd langgraph_modular_rag
```

---

## 3. 가상환경 생성 및 활성화

```powershell
# python 버전 고정
uv python pin 3.12
# 확인
Get-Content .python-version

# uv 초기화
uv init

# Python 3.12 기준 가상환경 생성
uv venv .venv --python 3.12 --prompt .venv

# 가상환경 활성화
.venv\Scripts\Activate.ps1
```

> 활성화 후 터미널 앞에 `(.venv)` 가 표시되면 정상입니다.

- 가상환경 이름 변경
```powershell
# 파일 열기
notepad .venv\pyvenv.cfg

# 설정 변경
prompt = .venv
```
- 가상환경 삭제[참고]
```powershell

Remove-Item -Recurse -Force .venv
# 파이썬 고정 파일 삭제
Remove-Item -Force .python-version -ErrorAction SilentlyContinue
# PowerShell 세션에 남아 있을 수 있는 환경변수 제거
Remove-Item Env:\VIRTUAL_ENV -ErrorAction SilentlyContinue
Remove-Item Env:\UV_PROJECT_ENVIRONMENT -ErrorAction SilentlyContinue
```
---

## 4. 패키지 설치
- 프로젝트 의존성 추가하려면 uv add로 설치하기
- pyproject.toml 파일에 기록을함.

```powershell
uv add langchain langchain-openai langchain-community
uv add langgraph
uv add faiss-cpu
uv add jupyter notebook ipykernel
uv add python-dotenv
uv add tiktoken
uv add rank_bm25
uv add chromadb langchain-chroma   # Advanced RAG - ChromaDB
uv add flashrank                   # Advanced RAG - Reranking
uv add langchain-text-splitters    # 텍스트 분할
uv add pypdf
```

- 한 번에 설치:

```powershell
uv add langchain langchain-openai langchain-community langgraph faiss-cpu jupyter notebook ipykernel python-dotenv tiktoken rank_bm25 chromadb langchain-chroma flashrank langchain-text-splitters pybdf
```

- 설치한 패키지 버전확인
```powershell
uv pip show langchain
```

---

## 5. Jupyter 커널 등록 및 삭제
- 등록
```powershell
python -m ipykernel install --user --name .venv --display-name "modular_rag(venv12)"

# 확인
jupyter kernelspec list
```
- 삭제[참고]
```
jupyter kernelspec uninstall .venv
```
---

## 6. OpenAI API 키 설정

프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 입력합니다.

```
OPENAI_API_KEY=sk-...여기에_본인_키_입력...
```

> `.env` 파일은 절대 GitHub 등 외부에 공유하지 마세요.

코드에서는 다음과 같이 불러옵니다:

```python
from dotenv import load_dotenv
load_dotenv(overide=True)
```

---

## 7. Jupyter Notebook 실행

```powershell
jupyter notebook
```

브라우저에서 자동으로 열리며, 커널은 `Python (modular_rag)` 를 선택합니다.

---

## 8. 폴더 구조

```
langgraph_modular_rag/
├── .env.local            # API 키 (.env 수정해서 쓰기)
├── .venv/                # 가상환경
├── 환경셋팅.md
├── part1_langchain_basic/
├── part2_naive_rag/
├── part3_advanced_rag_trend/
├── part4_langgraph_basic/
├── part5_langgraph_naver_shopping
└── part6_modular_rag_manual/
```

---

## 설치 패키지 요약

| 패키지 | 용도 |
|---|---|
| langchain | LangChain 핵심 |
| langchain-openai | OpenAI 연동 |
| langchain-community | 커뮤니티 컴포넌트 (문서 로더 등) |
| langgraph | LangGraph (Modular RAG) |
| faiss-cpu | 벡터 스토어 |
| jupyter / notebook | 실습 환경 |
| ipykernel | Jupyter 커널 |
| python-dotenv | .env 파일 로드 |
| tiktoken | 토큰 계산 |
| rank_bm25 | BM25 검색 (Advanced RAG) |
| chromadb / langchain-chroma | ChromaDB 벡터 스토어 (Advanced RAG) |
| flashrank | 로컬 Reranker (Advanced RAG) |
| langchain-text-splitters | 텍스트 분할 |
