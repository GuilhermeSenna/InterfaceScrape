import streamlit as st
import streamlit.components.v1 as stc
import datetime
import time
import requests
from bs4 import BeautifulSoup
import SessionState
import os.path
import json
from BuscarExemplo import buscar_exemplo
from Mineracao import minerar
from Mineracao.auxiliares import exemplo, espaco
from PIL import Image, ImageDraw, ImageFont

# lyrics += str(lyric).lower().replace('<p>', '').replace('</p>', '').replace('<br/>', ' ').replace('(', '').replace(')', '').replace(',', '') + ' '

# Variáveis auxiliares/globais
ultimo_scrap = {}
cont = 0

# req -> Armazenar a última requisição para não ser feita outra igual
# last_URL -> Último link salvo
session_state = SessionState.get(req='', last_URL=None)
# URL_multiplas = []
unicidade = ''
QNTD = 0
x = {}
text_save = []

# Constantes utilizadas para ser restaurado o último scrap
PRE_URL = ''
PRE_QNTD = 1
PRE_NOME = [''] * 10
PRE_UNICA = [False] * 10
PRE_TAG = [0] * 10
PRE_IDEEL = [1] * 10
PRE_NOIDE = [''] * 10


# Função que mostra o último scrape utilizado no topo da página
def carregar(arquivo):
    try:
        with open(arquivo) as json_file:
            data = json.load(json_file)

        my_expander = st.beta_expander("Último Scrap usado:", expanded=True)
        with my_expander:
            st.json(json.dumps(data, indent=4))

        return data
    except ValueError:
        st.error('Erro com o carregamento do arquivo JSON, tente com outro.')


# Função utilizada para recarregar na página o último scrape utilizado
def recarregar(data):
    global PRE_URL, PRE_QNTD, PRE_NOME, PRE_TAG, PRE_IDEEL, PRE_NOIDE, PRE_UNICA

    PRE_URL = data['URL']
    PRE_QNTD = data['qntd_inputs']

    for k, v in enumerate(data['nome']):
        PRE_NOME[k] = v

    for k, v in enumerate(data['TAG']):
        PRE_TAG[k] = v
        PRE_TAG[k] = ['div', 'span', 'a', 'img', 'input', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i',
                      'outro'].index(PRE_TAG[k])

    for k, v in enumerate(data['unica']):
            PRE_UNICA[k] = v

    for k, v in enumerate(data['ident_elemento']):
        PRE_IDEEL[k] = v
        PRE_IDEEL[k] = ['class', 'id', 'outro'].index(PRE_IDEEL[k])

    for k, v in enumerate(data['nome_ident']):
        PRE_NOIDE[k] = v


# Função basicamente de debug, pra o botão Buscar tags
def tagsMultiplas(URL, headers, tGlobal, tEspecifico, nEspecifico, c):
    global cont
    cont += 1

    # Testar antes se realmente há múltiplas tags
    if st.button('Buscar tags', key=cont):
        try:
            page = requests.get(URL, headers=headers)
        except:
            print('Deu problema')

        soup = BeautifulSoup(page.text, 'html.parser')

        conjunto = soup.findAll(tGlobal[c], attrs={tEspecifico[c]: nEspecifico[c]})

        for item in conjunto:
            st.text(item.text)


# Config:
# True: Utilizado para configurações que geram resultados (metodoManual)
# False: Usado para ver os resultados (carregamento_JSON)
def import_export(config):

    # Pasta em que é buscado os scraps
    pasta = './scraps'

    # Opção inicial/Default, não mostrar nenhum
    scrapers = ['Nenhum']

    # Se entrou para configuração
    if config:
        # Adiciona a opção de escolher o último scrape usado
        scrapers.append('Último usado')

        # Percorre a pasta buscando os arquivos que NÃO contenham "result" no nome, para receber as configuração de scrape
        for diretorio, subpastas, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                if not 'result' in arquivo:
                    scrapers.append(arquivo)

        # Escolha do arquivo
        archive = st.selectbox('(opcional) Escolha um arquivo salvo de scrap', scrapers)

        # Escolher usar ou não o último scrape
        if archive != scrapers[0] and archive != scrapers[1]:
            data = carregar('scraps/' + archive)
            if data:
                recarregar(data)
        elif archive == scrapers[1]: # Não é usado else pois existe também a opção de não mostrar nenhum scrape.
            data = carregar('scraps/ult_scrap.json')
            if data:
                recarregar(data)
    else:
        # Percorre a pasta buscando os arquivos que contenham "result" no nome, para visualização dos resultados
        for diretorio, subpastas, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                if 'result' in arquivo:

                    scrapers.append(arquivo)

        # Escolha do arquivo
        archive = st.selectbox('Escolha um dos resultados de scrape', scrapers)

        if archive != scrapers[0]:                # Se não for a opção "Nenhum"
            data = carregar('scraps/' + archive)  # Carrega o arquivo
            return data                           # O conteúdo de data é validado na função que é retornado (carregamento_JSON)
        else:                                     # Se for a opção "Nenhum"
            st.warning('Por favor escolha um arquivo para visualizá-lo')


# Função 'main'
def metodoManual(headers):
    global QNTD

    # Título do app
    st.title('Metodo manual')

    # Variável responsável por receber os dados do último scrape
    # print(data)

    import_export(True)

    # URL/Link informada para scrape
    URL = st.text_input('URL do site', PRE_URL)

    qntd_inputs = st.number_input('Digite a quantidade de inputs', value=PRE_QNTD, min_value=1, max_value=10, step=1)

    espaco()

    # Escolher se vai scrapear uma só página ou mais
    unicidade = st.radio('Página(s) única ou múltiplas?', ('única', 'múltiplas em sequência', 'múltiplas avulsas'))

    URL_base = complemento = ''

    # Lógica para múltiplas
    if unicidade == 'múltiplas em sequência':
        URL_base = st.text_input('URL de base ex: "google.com.br": ')

        complemento = st.text_input('Complemento do URL: ')

        QNTD = qntd_pags = st.text_input('Digite a quantidade de páginas a mais a serem buscadas: ')

        if st.button('testar tags'):
            # URL_multiplas.append(URL)
            for c in range(int(qntd_pags)):
                # URL_multiplas.append(f'{URL_base}{complemento}{c+2}')
                st.text(f'\n{URL_base}{complemento}{c + 2}')
    elif unicidade == 'múltiplas avulsas':
        paginas = st.text_area('Digite as páginas')

        if st.button('teste'):
            for pagina in paginas:
                print(pagina)

    espaco()
    exemplo()
    espaco()

    # Declaração de variáveis
    nome = ['']*10
    unica = ['']*10
    tipo_global = ['']*10
    tipo_especifico = ['']*10
    nome_especifico = ['']*10

    # Gerando inputs dinamicamente
    for c in range(0, int(qntd_inputs)):
        # Informando o nº do input a ser preenchido
        st.header('input ' + str(c + 1))

        # Nome da variável, afim de registrar no JSON
        nome[c] = st.text_input('Nome associado ao input (ex: Título, preço, Descrição, etc...) ', PRE_NOME[c], key=c)

        # Tag única ou não

        unica[c] = st.checkbox('tag única? (Não há outras tags com o mesmo identificador)', PRE_UNICA[c],
                            key=c)

        # Tipo da tag usada
        tipo_global[c] = st.selectbox('Selecione a tag',
                                      ['div', 'span', 'a', 'img', 'input', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i',
                                       'outro'],
                                      PRE_TAG[c], key=c)

        # Identificador da tag usada
        tipo_especifico[c] = st.selectbox('Selecione o identificador do elemento', ['class', 'id', 'outro'], key=c)

        # Nome do identificador
        nome_especifico[c] = st.text_input(" Nome do identificador usado", PRE_NOIDE[c], key=c)

        # Debug para caso haja múltiplas tags a serem obtidas
        if not unica[c]:
            tagsMultiplas(URL, headers, tipo_global, tipo_especifico, nome_especifico, c)

        espaco()

    # Opcionalidades para o usuário
    baixar = st.checkbox('Deseja baixar o arquivo .JSON?')
    limpar = st.checkbox('Deseja forçar a deleção de "\ n" e "\ t"? ')

    # Função principal de mineração
    minerar(URL, headers, unica, qntd_inputs, tipo_global, tipo_especifico, nome, nome_especifico, baixar, limpar,
            URL_base, complemento, False, ultimo_scrap, 2, x, QNTD, text_save)


def carregamento_JSON():
    st.title('Carregamento de JSON')

    data = import_export(False)

    if data:
        cont = -1
        verificar = False

        teste = []
        for i, (key, value) in enumerate(data.items()):
            # print(key, len([item for item in value if item]))

            teste.append(value)

            if cont == -1:
                cont = len([item for item in value if item])
            elif cont == len([item for item in value if item]):
                verificar = True
            else:
                verificar = False

        if verificar:
            st.success('Todos os atributos possuem a mesma quantidade de itens')
        else:
            st.warning('Há atributos com quantidade de itens diferentes')

        for c in range(len(teste[0])):
            cols = st.beta_columns(4)
            cols[0].write(f'{teste[0][c]}')
            cols[1].write(f'{teste[1][c]}')


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }

    st.set_page_config(page_title='Data Science', layout='wide')

    st.sidebar.title('Menu')

    selected = st.sidebar.radio('Selecione a página', ['Manual', 'Carregar JSON', 'Buscar exemplo', 'Imagem'])

    if selected == 'Manual':
        metodoManual(headers)
    elif selected == 'Carregar JSON':
        carregamento_JSON()
    elif selected == 'Buscar exemplo':
        buscar_exemplo(headers, session_state)
    elif selected == 'Imagem':
        pass
    else:
        st.title('Webscraping Automatico')


if __name__ == '__main__':
    main()
