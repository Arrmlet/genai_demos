import streamlit as st
from finttech_llama_index_assistant.fintech_assistant import agent

# Function to format the chat message with HTML
def format_message(author, message):
    if author == "You":
        return f'<div style="text-align: right; padding: 0.5em; "><b>{author}:</b> {message}</div>'
    else:  # AI
        return f'<div style="text-align: left; padding: 0.5em; color: green;"><b>{author}:</b> {message}</div>'


def main():
    import streamlit as st
    import os
    with st.sidebar:
        # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        st.text("🚀 Your real-time fintech assistant")
        if st.button('Back to Main Page'):
            st.query_params['app'] = 'main'

    st.title("💬 Fintech bot")
    st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = agent.query(prompt)
                msg = response.response

                ch_loc = 'charts/chart.json'
                if os.path.exists(ch_loc):
                    # Read the HTML file content
                    import plotly.io as pio
                    b = open('charts/chart.json', 'rb').read()
                    fig = pio.from_json(b)
                    st.plotly_chart(fig)
                    os.remove(ch_loc)

                placeholder = st.empty()
                full_response = ''
                for item in msg:
                    full_response += item
                    placeholder.markdown(full_response)
                # placeholder.markdown(full_response)
                # st.session_state.messages.append({"role": "assistant", "content": msg})
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
            # st.chat_message("assistant").write(msg)

if __name__ == "__main__":
    main()
