import requests
import pandas

from bs4 import BeautifulSoup

url = 'https://www.amazon.com/'
headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    }
# Get all data on Movee website
respone = requests.get(url,headers = headers)
print(respone)
soup = BeautifulSoup(respone.content, 'lxml')
titles = soup.findAll('div',id='desktop-1')

for title in titles:
    print(title)
# for title in titles:
#     print(title)
#     print('*************************************************************')

# Get detailed movie site http link

#print(links)
