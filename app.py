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

# Configurações do app
st.set_page_config(page_title="Sinalizador BTC", layout="centered")
st.title("🚦 Sinalizador de Risco - Bitcoin")
st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Campo para inserir API key
api_key = st.text_input("🔑 Insira sua API Key do CryptoPanic:", type="password")

# Só executa se a API key for preenchida
if api_key:
    with st.spinner("🔍 Coletando e analisando..."):
        # Coleta e análise
        noticias = buscar_noticias(api_key)
        sentimentos = analisar_sentimentos(noticias)
        volatilidade_real = obter_volatilidade_real()
        volume = len(sentimentos)
        mensagem, emoji = classificar_risco(sentimentos, volatilidade_real, volume)

    # Mostrar resultado textual
    st.markdown(f"## {emoji} {mensagem}")
    st.metric("Sentimento Médio", f"{np.mean(sentimentos):.2f}")
    st.metric("Volatilidade Estimada", f"{volatilidade_real:.2%}")
    st.metric("Volume de Notícias", volume)

    # Escolher imagem do semáforo com base no emoji (uso de 'in' para segurança)
    if "🔴" in emoji:
        imagem_risco = "images/semaforo_vermelho.jpeg"
    elif "🟡" in emoji:
        imagem_risco = "images/semaforo_amarelo.jpeg"
    elif "🟢" in emoji:
        imagem_risco = "images/semaforo_verde.jpeg"
    else:
        imagem_risco = "images/semaforo_verde.jpeg"  # fallback

    # Exibir imagem
    image = Image.open(imagem_risco)
    st.image(image, caption=f"Status de Risco: {mensagem}", use_container_width=True)

    # Mostrar as últimas notícias
    st.subheader("📰 Últimas Notícias")
    for i, noticia in enumerate(noticias[:10], 1):
        st.markdown(f"**{i:02d}.** {noticia}")
else:
    st.info("Para começar, insira sua chave da API do CryptoPanic.")


