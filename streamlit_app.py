import streamlit as st
import openai

def generate_response(prompt, api_key):
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="gpt-4",  # Byt till "gpt-4" om tillgängligt
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Generisk GPT-4 Assistent")
    st.write("Ställ en fråga eller be om hjälp!")

    # Input field for API key
    api_key = st.text_input("Ange din OpenAI API-nyckel här:", type="password")

    # Check if API key is provided
    if not api_key:
        st.warning("Vänligen ange din API-nyckel.")
        return

    user_input = st.text_area("Din fråga:", "", height=200)
    
    if st.button("Skicka"):
        if user_input:
            with st.spinner("Genererar svar..."):
                response = generate_response(user_input, api_key)
                st.write("**Svar:**")
                st.write(response)
        else:
            st.write("Vänligen skriv en fråga först.")

if __name__ == "__main__":
    main()
