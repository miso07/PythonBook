import requests

url = "https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=btc_krw"
response = requests.get(url)

coin = response.json()
print(coin)
print(coin['last'])
print(coin['volume'])


