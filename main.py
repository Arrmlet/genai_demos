import streamlit as st
import rag_chatbot_app
import fintech_streamlit_page

st.set_page_config(page_title='GenAI Solutions Demo', layout='wide')

def main():
    st.markdown(
        """
        <style>
        .header {
            font-size: 48px;
            font-weight: bold;
            color: #FF5722;
            text-align: center;
            margin-bottom: 50px;
        }
        .app-card {
            background-color: #FFFFFF;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 30px;
            text-align: center;
            transition: transform 0.3s;
            margin-bottom: 30px;
        }
        .app-card:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        }
        .app-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #333333;
        }
        .app-description {
            font-size: 16px;
            color: #666666;
            margin-bottom: 30px;
        }
        .app-button {
            display: inline-block;
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            text-decoration: none;
            color: #FFFFFF;
            background-color: #FF5722;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .app-button:hover {
            background-color: #E64A19;
        }
        .app-image-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 30px;
        }
        .app-image {
            width: 200px;
            height: 200px;
            object-fit: cover;
            border-radius: 50%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="header">GenAI Solutions Demo</div>', unsafe_allow_html=True)

    apps = [
        {
            'title': 'RAG Chatbot for software company',
            'description': 'Explore the RAG Chatbot application that enhace customer support of HowSimpl Company.',
            'url': '?app=rag_chatbot',
            'image': 'https://howsimpl.com/wp-content/uploads/2022/01/center-logo.svg'
        },
        {
            'title': 'Voice-to-Voice RAG',
            'description': 'Experience the Voice-to-Voice RAG application.',
            'url': '?app=voice_to_voice_rag',
            'image': 'https://images.unsplash.com/photo-1558494949-ef01cbfbd65b?w=200&h=200&fit=crop'
        },
        {
            'title': 'RealTime Finance assistant',
            'description': 'Discover the future of Fintech.',
            'url': '?app=future_app',
            'image': 'https://americandeposits.com/wp-content/uploads/what-is-fintech-square.jpg'
        }
    ]

    app_grid = st.container()

    with app_grid:
        for i in range(0, len(apps), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(apps):
                    app = apps[i + j]
                    with cols[j]:
                        st.markdown(
                            f'<div class="app-card">'
                            f'<div class="app-image-container">'
                            f'<img src="{app["image"]}" class="app-image">'
                            f'</div>'
                            f'<div class="app-title">{app["title"]}</div>'
                            f'<div class="app-description">{app["description"]}</div>'
                            f'<a href="{app["url"]}" target="_self" class="app-button">Launch App</a>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

def voice_to_voice_rag():
    st.title('Voice-to-Voice RAG')
    st.write('Welcome to the Voice-to-Voice RAG application!')

    # Add a file uploader for audio files
    audio_file = st.file_uploader('Upload an audio file', type=['wav', 'mp3'])

    if audio_file:
        # Placeholder response for testing
        st.write(f"Uploaded audio file: {audio_file.name}")

    # Add a button to go back to the main page
    if st.button('Back to Main Page'):
        st.query_params['app'] = 'main'

def future_app():
    st.title('Future App')
    st.write('Welcome to the Future App application!')

    # Add a placeholder feature for testing
    st.write('This is a placeholder feature for the Future App.')

    # Add a button to go back to the main page
    if st.button('Back to Main Page'):
        st.query_params['app'] = 'main'

if __name__ == '__main__':
    #app = st.experimental_get_query_params().get('app', ['main'])[0]
    app = st.query_params.get('app', 'main')
    if app == 'main':
        main()
    elif app == 'rag_chatbot':
        rag_chatbot_app.main()
    elif app == 'voice_to_voice_rag':
        voice_to_voice_rag()
    elif app == 'future_app':
        # future_app()
        fintech_streamlit_page.main()
