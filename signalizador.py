import requests

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

from transformers import pipeline, BertTokenizer, BertForSequenceClassification

# Carregar modelo BERT
tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
sentiment_pipeline = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

def analisar_sentimentos(noticias):
    sentimentos = []
    for noticia in noticias:
        resultado = sentiment_pipeline(noticia)[0]
        score = resultado['score']
        label = resultado['label']
        # Converter estrelas para sentimento numérico
        if label in ['1 star', '2 stars']:
            sentimentos.append(-score)
        elif label in ['4 stars', '5 stars']:
            sentimentos.append(score)
        else:
            sentimentos.append(0)
    return sentimentos
