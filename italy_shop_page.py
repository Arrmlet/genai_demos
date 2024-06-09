import requests
from config import settings
# Define the API endpoint

API_ENDPOINT = settings.italy_shop_url


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
        st.text("")
        st.link_button('Website', 'https://www.piscinemilano.com/')
        if st.button('Back to Main Page'):
            st.query_params['app'] = 'main'

    st.title("💬 PiscineMilano versione di prova del chatbot")
    st.caption("🚀")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Come posso aiutarla?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = get_rag_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(msg["content"])



if __name__ == "__main__":
    main()