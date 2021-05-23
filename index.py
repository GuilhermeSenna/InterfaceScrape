import streamlit as st
import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup
import SessionState
import os.path
from autoscraper import AutoScraper
import json
from BuscarExemplo import buscar_exemplo
from Mineracao import minerar
from Mineracao.auxiliares import exemplo, espaco

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
PRE_NOME = ['', '', '', '', '', '', '', '', '', '']
PRE_UNICA = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
PRE_TAG = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
PRE_IDEEL = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
PRE_NOIDE = ['', '', '', '', '', '', '', '', '', '']


# Função que mostra o último scrape utilizado no topo da página
def ultimo_scrape():
    try:
        with open('ult_scrap.txt') as json_file:
            data = json.load(json_file)

        my_expander = st.beta_expander("Último Scrap usado:", expanded=True)
        with my_expander:
            # clicked = my_widget("second")
            st.json(json.dumps(data, indent=4))

        # st.subheader("Último Scrap usado:")



        return data
    except:
        pass


# Função usada para perguntar para o usuário se ele quer usar ou não o último scrape
def usar_ultimo(data):
    ult = st.radio('Usar último scrape?', ('nao', 'sim'))

    if ult == 'sim':
        recarregar(data)


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
        PRE_UNICA[k] = ['sim', 'nao'].index(PRE_UNICA[k])

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


# Função 'main'
def metodoManual(headers):
    global QNTD

    # Coloca o título na página
    st.title('Webscraping Manual')

    # Variável responsável por receber os dados do último scrape
    data = ultimo_scrape()

    pasta = './scraps'

    scrapers = []
    scrapers.append('')

    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            # print(os.path.join(diretorio, arquivo))
            if not 'result' in arquivo:
                scrapers.append(arquivo)

    # print(scrapers)

    st.selectbox('Escolha um arquivo salvo de scrap', scrapers)

    # Escolher usar ou não o último scrape
    usar_ultimo(data)

    # URL/Link informada para scrape
    URL = st.text_input('URL do site', PRE_URL)

    # with st.form("my_form"):
    #     st.write("Inside the form")
    #     slider_val = st.slider("Form slider")
    #     checkbox_val = st.checkbox("Form checkbox")
    #
    #
    #     submitted = st.form_submit_button("Submit")
    #     if submitted:
    #         st.write("slider", slider_val, "checkbox", checkbox_val)
    #
    # st.write("Outside the form")

    # Quantidade de inputs a ser scrapeado
    qntd_inputs = st.number_input('Digite a quantidade de inputs', value=PRE_QNTD, min_value=1, max_value=10, step=1)
    # qntd_inputs = st.text_input('Digite a quantidade de inputs (Por padrão é deixado 1)', PRE_QNTD)

    #
    # if qntd_inputs == '':
    #     qntd_inputs = 1

    # agrupamento = st.radio(' Qual a forma de agrupamento a ser usada?', ('Linear', 'Conjuntos', 'Mista'))

    espaco(st)

    # Escolher se vai scrapear uma só página ou mais
    unicidade = st.radio('Página única ou múltipla?', ('única', 'múltipla'))

    URL_base = complemento = ''

    # Lógica para múltiplas
    if unicidade == 'múltipla':
        URL_base = st.text_input('URL de base ex: "google.com.br": ')

        complemento = st.text_input('Complemento do URL: ')

        QNTD = qntd_pags = st.text_input('Digite a quantidade de páginas a mais a serem buscadas: ')

        if st.button('testar tags'):
            # URL_multiplas.append(URL)
            for c in range(int(qntd_pags)):
                # URL_multiplas.append(f'{URL_base}{complemento}{c+2}')
                st.text(f'\n{URL_base}{complemento}{c + 2}')

    espaco(st)

    exemplo(st)

    espaco(st)

    #                                                                                          #
    #                      Início da criação das variáveis para guardar os inputs/tags         #
    #                      Até o momento o limite são 10 inputs                                #
    #                                                                                          #

    nome1 = nome2 = nome3 = nome4 = nome5 = nome6 = nome7 = nome8 = nome9 = nome10 = ''
    nome = [nome1, nome2, nome3, nome4, nome5, nome6, nome7, nome8,
            nome9, nome10]
    englobado1 = englobado2 = englobado3 = englobado4 = englobado5 = englobado6 = englobado7 = englobado8 = englobado9 = englobado10 = ''
    unica = [englobado1, englobado2, englobado3, englobado4, englobado5, englobado6, englobado7, englobado8,
             englobado9, englobado10]
    tipo_global1 = tipo_global2 = tipo_global3 = tipo_global4 = tipo_global5 = tipo_global6 = tipo_global7 = tipo_global8 = tipo_global9 = tipo_global10 = ''
    tipo_global = [tipo_global1, tipo_global2, tipo_global3, tipo_global4, tipo_global5, tipo_global6, tipo_global7,
                   tipo_global8, tipo_global9, tipo_global10]
    tipo_especifico1 = tipo_especifico2 = tipo_especifico3 = tipo_especifico4 = tipo_especifico5 = tipo_especifico6 = tipo_especifico7 = tipo_especifico8 = tipo_especifico9 = tipo_especifico10 = ''
    tipo_especifico = [tipo_especifico1, tipo_especifico2, tipo_especifico3, tipo_especifico4, tipo_especifico5,
                       tipo_especifico6, tipo_especifico7, tipo_especifico8, tipo_especifico9, tipo_especifico10]
    nome_especifico1 = nome_especifico2 = nome_especifico3 = nome_especifico4 = nome_especifico5 = nome_especifico6 = nome_especifico7 = nome_especifico8 = nome_especifico9 = nome_especifico10 = ''
    nome_especifico = [nome_especifico1, nome_especifico2, nome_especifico3, nome_especifico4, nome_especifico5,
                       nome_especifico6, nome_especifico7, nome_especifico8, nome_especifico9, nome_especifico10]

    #                                                                                     #
    #                      Fim da criação das variáveis                                   #
    #                                                                                     #

    # Gerando inputs dinamicamente
    for c in range(0, int(qntd_inputs)):
        # Informando o nº do input a ser preenchido
        st.subheader('input ' + str(c + 1))

        # Nome da variável, afim de registrar no JSON
        nome[c] = st.text_input('Nome associado ao input (ex: Título, preço, Descrição, etc...) ', PRE_NOME[c], key=c)

        # Tag única ou não
        unica[c] = st.radio('tag única? (Não há outras tags com o mesmo identificador)', ('sim', 'nao'), PRE_UNICA[c],
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
        if unica[c] == 'nao':
            tagsMultiplas(URL, headers, tipo_global, tipo_especifico, nome_especifico, c)

        espaco(st)

    # Opcionalidades para o usuário
    baixar = st.radio('Deseja baixar o arquivo .JSON?', ('nao', 'sim'))
    limpar = st.radio('Deseja forçar a deleção de "\ n" e "\ t"? ', ('nao', 'sim'))

    # Função principal de mineração
    minerar(URL, headers, unica, qntd_inputs, tipo_global, tipo_especifico, nome, nome_especifico, baixar, limpar,
            URL_base, complemento, False, st, ultimo_scrap, 2, x, QNTD, text_save)

    # y = st.radio('tag única? (Não há outras tags com o mesmo identificador)', ('sim', 'nao'))
    # if y == 'sim':
    #     print(session_state)
    # with open('data.txt', 'w') as outfile:
    #     json.dump(texto_formatado, outfile)


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }

    st.sidebar.title('Menu')

    selected = st.sidebar.radio('Selecione a página', ['Manual', 'Automatico', 'Carregar JSON', 'Buscar exemplo'])

    if selected == 'Manual':
        metodoManual(headers)
    elif selected == 'Carregar JSON':
        st.title('Carregamento de JSON')

        if st.button('teste'):
            with open('scraps/scrap8_result.json') as json_file:
                data = json.load(json_file)
                # print(data['Titulo'])
                # print(json.dumps(data, indent=4))
    elif selected == 'Buscar exemplo':
        buscar_exemplo(headers, st, session_state)
    else:
        st.title('Webscraping Automatico')


# Início aqui
main()
