import streamlit as st
import openai  # Se till att du har installerat openai-biblioteket

# Visa titel och beskrivning.
st.title("💬 Chatbot")
st.write(
    "Detta är en enkel chatbot som använder OpenAI:s GPT-4-modell för att generera svar. "
    "För att använda denna app behöver du tillhandahålla en OpenAI API-nyckel, som du kan få [här](https://platform.openai.com/account/api-keys). "
    "Du kan också lära dig hur du bygger denna app steg för steg genom att [följa vår handledning](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Be användaren om deras OpenAI API-nyckel via `st.text_input`.
# Alternativt kan du lagra API-nyckeln i `./.streamlit/secrets.toml` och komma åt den
# via `st.secrets`, se https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API-nyckel", type="password")
if not openai_api_key:
    st.info("Vänligen lägg till din OpenAI API-nyckel för att fortsätta.", icon="🗝️")
else:
    # Skapa en OpenAI-klient.
    openai.api_key = openai_api_key

    # Skapa en session state-variabel för att lagra chatmeddelanden. Detta säkerställer att
    # meddelandena kvarstår mellan körningar.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Visa befintliga chatmeddelanden via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Skapa ett chattinmatningsfält för att låta användaren skriva in ett meddelande. Detta visas
    # automatiskt längst ner på sidan.
    if prompt := st.chat_input("Vad vill du prata om?"):
        # Spara och visa den aktuella prompten.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generera ett svar med OpenAI API.
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )

        # Visa svaret i chatten och lagra det i session state.
        assistant_message = response['choices'][0]['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
