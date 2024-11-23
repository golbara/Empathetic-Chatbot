from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"],base_url="https://api.metisai.ir/api/v1/wrapper/{provider}")
client = OpenAI(
    api_key="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")
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})