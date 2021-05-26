import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }

URL = 'https://www.tecmundo.com.br/minha-serie/217972-black-clover-4-temporada-anime-ganha-data-estreia-adult-swim.htm'

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

print(soup.prettify())



# from ftfy import fix_encoding
#
# a = 'são não anúncio tão quão à'
# b = a.encode('utf-8')
# c = b.decode('utf-8')
#
# print(fix_encoding(a))

