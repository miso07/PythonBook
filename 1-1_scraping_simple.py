from bs4 import BeautifulSoup
import requests

url = "https://coinmarketcap.com/currencies/bitcoin/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

priceValue = soup.find('div', {'class': 'priceValue'})
coin_data = priceValue.find('span').get_text()
print(coin_data)

