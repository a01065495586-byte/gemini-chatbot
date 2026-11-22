# Gemini 터미널 챗봇 (`gemini-3.1-flash-lite`)

Google GenAI의 최신 **Interactions API** 및 **`gemini-3.1-flash-lite`** 모델을 활용한 터미널 대화형 챗봇입니다.  
사용자 가이드라인에 따라 **`uv`**를 기반으로 개발 및 실행됩니다.

---

## 🚀 빠른 시작

### 1. API 키 설정
[Google AI Studio](https://aistudio.google.com/apikey)에서 무료 API 키를 발급받은 뒤, 프로젝트 루트에 `.env` 파일을 생성합니다.

```bash
cp .env.example .env
```
`.env` 파일 내용:
```env
GEMINI_API_KEY=실제_발급받은_API_키
```

### 2. 실행 방법 (`uv run` 사용)
패키지 설치 및 가상환경 활성화 과정 없이 `uv`를 통해 바로 실행할 수 있습니다:

```bash
uv run gemini-chatbot
```

또는 모듈 실행 방식:
```bash
uv run python -m gemini_chatbot.main
```

---

## 💬 대화 기능 및 명령어
- **멀티턴 문맥 유지**: Stateful 세션을 통해 이전 대화 내용을 기억합니다.
- **스트리밍 출력**: 모델의 답변이 실시간 타자 형식으로 출력됩니다.
- **명령어**:
  - `clear` 또는 `reset`: 대화 히스토리 초기화
  - `exit`, `quit`, `q`: 챗봇 종료

