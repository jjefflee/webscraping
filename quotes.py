from urllib.request import urlopen, Request
import requests 

url = 'https://quotes/toscrape.com/page/'

reponse = requests.get(url)

soup = BeautifulSoup 