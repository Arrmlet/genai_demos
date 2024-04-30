import streamlit as st

from audio_recorder_streamlit import audio_recorder

import base64

def main():
    st.sidebar.title('API KEY CONFIGURATION')
    api_key = st.sidebar.text_input('Enter your api key', type='password')
    st.sidebar.markdown('---')

    st.title('Opes Voice Assistant')
    st.write('Hi please record your message!!!!!')
    recorded_audio = audio_recorder()

    if recorded_audio:
        audio_file = 'vlad_test.mp3'
        with open(audio_file, 'wb') as f:
            f.write(recorded_audio)
        st.audio(audio_file)

if __name__ == '__main__':
    main()
