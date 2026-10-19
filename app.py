import streamlit as st
from openai import OpenAI


MODEL = "gpt-4o-mini"

st.set_page_config(page_title="AI 챗봇", page_icon="💬", layout="centered")


def get_client() -> OpenAI:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except KeyError as exc:
        raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다. Streamlit Cloud의 App settings > Secrets에 API 키를 등록해 주세요.") from exc
    if not api_key or not str(api_key).strip():
        raise RuntimeError("OPENAI_API_KEY가 비어 있습니다. Streamlit Secrets를 확인해 주세요.")
    return OpenAI(api_key=api_key)


def reset_chat() -> None:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}]


st.title("💬 AI 챗봇")
st.caption(f"OpenAI {MODEL} 모델을 사용합니다.")

with st.sidebar:
    st.subheader("설정")
    st.write("대화 내용은 현재 브라우저 세션에만 저장됩니다.")
    if st.button("대화 초기화", use_container_width=True):
        reset_chat()
        st.rerun()

if "messages" not in st.session_state:
    reset_chat()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            client = get_client()
            response = client.chat.completions.create(model=MODEL, messages=st.session_state.messages, temperature=0.7, stream=True)
            answer = st.write_stream(chunk.choices[0].delta.content or "" for chunk in response)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as error:
            st.error(f"응답을 가져오지 못했습니다: {error}")
