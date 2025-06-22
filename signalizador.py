import requests
from transformers import pipeline, BertTokenizer, BertForSequenceClassification
import numpy as np

# Carregar modelo BERT
tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
sentiment_pipeline = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

def buscar_noticias(api_key, limite=20):
    url = 'https://cryptopanic.com/api/v1/posts/'
    parametros = {
        'auth_token': api_key,
        'filter': 'news',
        'currencies': 'BTC',
        'kind': 'news'
    }
    resposta = requests.get(url, params=parametros)
    if resposta.status_code == 200:
        dados = resposta.json()
        titulos = [noticia['title'] for noticia in dados.get('results', [])]
        return titulos[:limite]
    else:
        print("Erro ao buscar notícias:", resposta.status_code)
        return []

def analisar_sentimentos(noticias):
    sentimentos = []
    for noticia in noticias:
        resultado = sentiment_pipeline(noticia)[0]
        score = resultado['score']
        label = resultado['label']
        if label in ['1 star', '2 stars']:
            sentimentos.append(-score)
        elif label in ['4 stars', '5 stars']:
            sentimentos.append(score)
        else:
            sentimentos.append(0)
    return sentimentos

def classificar_risco(sentimentos, volatilidade_estimada, volume_noticias):
    if volume_noticias == 0:
        return "Sem dados suficientes", "⚪"

    sentimento_medio = np.mean(sentimentos)

    if abs(sentimento_medio) > 0.6 and volume_noticias > 20:
        return "🔴 Alta Volatilidade - Evite operar", "🔴"
    elif 0.3 < abs(sentimento_medio) <= 0.6 or volume_noticias > 10:
        return "🟡 Cuidado - Mercado instável", "🟡"
    else:
        return "🟢 Mercado calmo - Bom para operar", "🟢"

