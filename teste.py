from bs4 import BeautifulSoup
import requests
import re

page = requests.get('https://mises.org.br/article/3340/nos-150-anos-da-revolucao-marginalista-um-resumo-de-suas-cruciais-constatacoes')

soup = BeautifulSoup(page.text, 'html.parser')

for t in soup.findAll(text=re.compile('nos 150 anos', re.IGNORECASE)):
    print(t.parent.attrs)