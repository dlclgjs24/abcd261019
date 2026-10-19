# Streamlit OpenAI 챗봇

`gpt-4o-mini`를 사용하는 Streamlit 챗봇입니다.

## Streamlit Community Cloud 배포

1. 이 저장소를 Streamlit Community Cloud에서 선택합니다.
2. Main file path에 `app.py`를 입력합니다.
3. App settings > Secrets에 아래 내용을 등록합니다.

```toml
OPENAI_API_KEY = "sk-..."
```

API 키는 GitHub 저장소에 업로드하지 마세요.
