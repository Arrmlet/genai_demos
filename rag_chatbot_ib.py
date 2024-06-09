import requests
from config import settings
# Define the API endpoint

API_ENDPOINT = settings.nastya_rag_url


# Function to make the API call
def get_rag_response(user_input):
    payload = {"q": user_input}
    response = requests.post(API_ENDPOINT, json=payload)
    if response.status_code == 200:
        return response.json()["full_answer"]
    else:
        return "Sorry, an error occurred while processing your request."


def main():
    import streamlit as st
    with st.sidebar:
        # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        st.text("🚀 Привіт, це ШІ чат бот для найкращої PPC спеціалістки в Україні.")
        st.link_button('Insta', 'https://t.me/hs_education_bot')
        st.link_button('Telegram bot', 'https://t.me/hs_education_bot')
        if st.button('Back to Main Page'):
            st.query_params['app'] = 'main'

    st.title("💬 Ви готові йти в ногу з часом, та трансформувати ваш бізнес?")
    st.caption("🚀")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Як я можу вам допомогти?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = get_rag_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(msg)


if __name__ == "__main__":
    main()