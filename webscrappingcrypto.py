import requests
from bs4 import BeautifulSoup

def scrape_coinmarketcap():
    url = 'https://coinmarketcap.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        crypto_rows = soup.find_all('tr', class_='cmc-table-row')

        for row in crypto_rows[:5]: 
            name = row.find('p', class_='coin-item-symbol').text.strip()
            symbol = row.find('p', class_='coin-item-symbol').text.strip()
            price = row.find('div', class_='price___3rj7O').text.strip()
            percent_change = row.find('td', class_='percent-change-24h').text.strip()

           
            percent_change_value = float(percent_change.replace('%', ''))

            
            price_value = float(price.replace('$', '').replace(',', ''))
            new_price = price_value + (percent_change_value / 100 * price_value)

            
            print(f"Name: {name}")
            print(f"Symbol: {symbol}")
            print(f"Price: {price}")
            print(f"Percent Change (24h): {percent_change}")
            print(f"Corresponding Price (Based on % Change): {new_price:.2f}")
            print("\n")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_coinmarketcap()
