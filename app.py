import streamlit as st
from datetime import datetime
import numpy as np
from PIL import Image

# Importa funções do arquivo signalizador.py
from signalizador import (
    buscar_noticias,
    analisar_sentimentos,
    classificar_risco,
    obter_volatilidade_real
)

# Configuração do app
st.set_page_config(page_title="Sinalizador BTC", layout="centered")
st.title("🚦 Sinalizador de Risco - Bitcoin")
st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Exibir imagem do semáforo
image = Image.open("images/btc_semaforo.jpeg")
st.image(image, caption="Sinalizador BTC", use_column_width=True)

# Campo para inserir a API Key
api_key = st.text_input("🔑 Insira sua API Key do CryptoPanic:", type="password")

# Quando a API key for preenchida:
if api_key:
    with st.spinner("🔍 Coletando e analisando..."):
        # Coleta e processamento
        noticias = buscar_noticias(api_key)
        sentimentos = analisar_sentimentos(noticias)
        volatilidade_real = obter_volatilidade_real()
        volume = len(sentimentos)
        mensagem, emoji = classificar_risco(sentimentos, volatilidade_real, volume)

    # Exibir resultado
    st.markdown(f"## {emoji} {mensagem}")
    st.metric("Sentimento Médio", f"{np.mean(sentimentos):.2f}")
    st.metric("Volatilidade Estimada", f"{volatilidade_real:.2%}")
    st.metric("Volume de Notícias", volume)

    # Mostrar últimas notícias analisadas
    st.subheader("📰 Últimas Notícias")
    for i, noticia in enumerate(noticias[:10], 1):
        st.markdown(f"**{i:02d}.** {noticia}")
else:
    st.info("Para começar, insira sua chave da API do CryptoPanic.")

