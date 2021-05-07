from autoscraper import AutoScraper

url = 'https://mises.org.br/article/3340/nos-150-anos-da-revolucao-marginalista-um-resumo-de-suas-cruciais-constatacoes'

wanted_list = ["No entanto, mesmo estes conceitos básicos, porém cruciais, seguem sendo mal compreendidos."]

scraper = AutoScraper()
print(scraper.build(url, wanted_list))
