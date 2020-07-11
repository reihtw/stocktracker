import requests, json

pagina = requests.get(f'https://bovespa.nihey.org/api/quote/ABEV3/2020-06-05')
x = pagina.content
y = json.loads(x)
print(y['codneg'])