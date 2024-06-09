import os
from pathlib import Path
import streamlit as st


class Settings:
    openai_api = st.secrets.get('openai_api', '')
    news_api = st.secrets.get('news_api', '')
    howsimpl_rag_url = st.secrets.get('howsimpl_rag_url', '')
    nastya_rag_url = st.secrets.get('nastya_rag_url', '')
    italy_shop_url = st.secrets.get('italy_shop_url', '')


settings = Settings()
