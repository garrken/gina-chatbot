import streamlit as st
import openai
from typing import List, Dict

# Visa titel och beskrivning.
st.title("💬 Omnichat GPT-4 Chatbot")
st.write(
    "Detta är en chatbot-applikation som använder OpenAI:s GPT-4-modell för att generera svar. "
    "För att använda denna app behöver du ange din OpenAI API-nyckel."
)

# Be användaren om deras OpenAI API-nyckel via `st.text_input`.
openai_api_key = st.text_input("OpenAI API-nyckel", type="password")

# Kontrollera om API-nyckeln har angetts.
if not openai_api_key:
    st.info("Vänligen ange din OpenAI API-nyckel för att fortsätta.", icon="🗝️")
else:
    openai.api_key = openai_api_key

    # Initiera session state för att lagra meddelanden.
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    # Funktion för att kalla OpenAI API och få svar
    def get_chatgpt_response(messages: List[Dict[str, str]]) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Byt till "gpt-3.5-turbo" om du inte har tillgång till GPT-4
            messages=messages,
        )
        return response.choices[0].message["content"]

    # Visa befintliga meddelanden.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Skapa ett chattinmatningsfält för användaren att skriva in ett meddelande.
    if prompt := st.chat_input("Skriv ditt meddelande här..."):
        # Lägg till användarens meddelande i sessionens state.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Hämta GPT-svar och visa det.
        assistant_message = get_chatgpt_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
