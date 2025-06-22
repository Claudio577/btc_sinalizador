from PIL import Image
import streamlit as st
from datetime import datetime
import random
import numpy as np
from signalizador import buscar_noticias, analisar_sentimentos, classificar_risco

st.set_page_config(page_title="Sinalizador BTC", layout="centered")
st.title("🚦 Sinalizador de Risco - Bitcoin")
st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

api_key = st.text_input("🔑 Insira sua API Key do CryptoPanic:", type="password")

if api_key:
    with st.spinner("🔍 Coletando e analisando..."):
        noticias = buscar_noticias(api_key)
        sentimentos = analisar_sentimentos(noticias)
        from signalizador import obter_volatilidade_real
        volatilidade_real = obter_volatilidade_real()
        volume = len(sentimentos)
        mensagem, emoji = classificar_risco(sentimentos, volatilidade_real, volume)

    st.markdown(f"## {emoji} {mensagem}")
    st.metric("Sentimento Médio", f"{np.mean(sentimentos):.2f}")
    st.metric("Volatilidade Estimada", f"{volatilidade_real:.2%}")
    st.metric("Volume de Notícias", volume)

    st.subheader("📰 Últimas Notícias")
    for i, noticia in enumerate(noticias[:10], 1):
        st.markdown(f"**{i:02d}.** {noticia}")
else:
    st.info("Para começar, insira sua chave da API do CryptoPanic.")
