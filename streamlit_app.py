import openai
import streamlit as st

st.title("💬 Chatbot")
st.write(
    "Detta är en enkel chatbot som använder OpenAI:s GPT-4-modell för att generera svar. "
    "För att använda denna app behöver du tillhandahålla en OpenAI API-nyckel, som du kan få [här](https://platform.openai.com/account/api-keys). "
)

openai_api_key = st.text_input("OpenAI API-nyckel", type="password")
if not openai_api_key:
    st.info("Vänligen lägg till din OpenAI API-nyckel för att fortsätta.", icon="🗝️")
else:
    openai.api_key = openai_api_key

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Vad vill du prata om?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )

        assistant_message = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
