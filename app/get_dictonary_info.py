
def get_words_from_phrase(phrase):
    url = "https://www.thai2english.com/api/search"

    # Parâmetros da consulta
    params = {
    "q": phrase
    }

    # Cabeçalhos da requisição
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-us",
    "Connection": "keep-alive",
    }

    r = requests.get(url, headers=headers, params=params)

    return r.text
