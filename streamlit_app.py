import streamlit as st
import openai  # Se till att du har den senaste versionen installerad

# Visa titel och beskrivning.
st.title("💬 AI-driven Chatbot")
st.write(
    "Detta är en enkel chatbot som använder OpenAI:s GPT-4-modell för att generera svar. "
    "För att använda denna app behöver du tillhandahålla en OpenAI API-nyckel, som du kan få [här](https://platform.openai.com/account/api-keys)."
)

# Be användaren om deras OpenAI API-nyckel via `st.text_input`.
openai_api_key = st.text_input("OpenAI API-nyckel", type="password")
if not openai_api_key:
    st.info("Vänligen lägg till din OpenAI API-nyckel för att fortsätta.", icon="🗝️")
else:
    openai.api_key = openai_api_key

    # Skapa en session state-variabel för att lagra chatmeddelanden.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Visa befintliga chatmeddelanden.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Skapa ett chattinmatningsfält för användaren att skriva in ett meddelande.
    if prompt := st.chat_input("Vad vill du prata om?"):
        # Spara och visa användarens meddelande.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generera ett svar med OpenAI API.
        response = openai.Completion.create(
            model="text-davinci-004",  # Använd GPT-4-modellen
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Få och visa assistentens svar.
        assistant_message = response.choices[0].text.strip()
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
