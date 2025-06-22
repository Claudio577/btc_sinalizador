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

