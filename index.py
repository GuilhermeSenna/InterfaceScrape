import streamlit as st
import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup
import SessionState
import os.path
from autoscraper import AutoScraper
import json

ultimo_scrap = {}
cont = 0
session_state = SessionState.get(texto='')

PRE_URL = ''
PRE_QNTD = 1
PRE_NOME = ['', '', '', '', '', '', '', '', '', '']
PRE_TAG = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
PRE_IDEEL = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
PRE_NOIDE = ['', '', '', '', '', '', '', '', '', '']


def espaco():
    st.text('-=' * 45)


def exemplo():
    st.subheader("Exemplo")
    st.text('<p class="paragraph"> Paragrafo qualquer </p> ')
    st.text('tag: p')
    st.text('identificador usado: class')
    st.text('Nome do identificador: paragraph')


def recarregar(data):
    global PRE_URL, PRE_QNTD, PRE_NOME, PRE_TAG, PRE_IDEEL, PRE_NOIDE

    PRE_URL = data['URL']
    PRE_QNTD = data['qntd_inputs']

    for k, v in enumerate(data['nome']):
        PRE_NOME[k] = v

    for k, v in enumerate(data['TAG']):
        PRE_TAG[k] = v
        PRE_TAG[k] = ['div', 'span', 'a', 'img', 'input', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
         'outro'].index(PRE_TAG[k])

    for k, v in enumerate(data['ident_elemento']):
        PRE_IDEEL[k] = v
        PRE_IDEEL[k] = ['class', 'id', 'outro'].index(PRE_IDEEL[k])

    for k, v in enumerate(data['nome_ident']):
        PRE_NOIDE[k] = v


def metodoManual(headers):
    st.title('Webscraping Manual')

    data = ''

    try:
        with open('ult_scrap.txt') as json_file:
            data = json.load(json_file)

        st.subheader("Último Scrap usado:")

        st.text(json.dumps(data, indent=4))
    except:
        pass

    ult = st.radio('Usar último scrape?', ('nao', 'sim'))

    if ult == 'sim':
        recarregar(data)

    URL = st.text_input('URL do site', PRE_URL)

    qntd_inputs = st.text_input('Digite a quantidade de inputs (Por padrão é deixado 1)', PRE_QNTD)
    #
    # if qntd_inputs == '':
    #     qntd_inputs = 1

    agrupamento = st.radio(' Qual a forma de agrupamento a ser usada?', ('Linear', 'Conjuntos', 'Mista'))

    espaco()

    exemplo()

    espaco()

    # Criação das variáveis para guardar os inputs/tags
    # Até o momento o limite são 10 inputs


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

    # Gerando inputs dinamicamente
    for c in range(0, int(qntd_inputs)):
        st.subheader('input ' + str(c + 1))

        nome[c] = st.text_input('Nome associado ao input (ex: Título, preço, Descrição, etc...) ', PRE_NOME[c], key=c)

        unica[c] = st.radio('tag única? (Não há outras tags com o mesmo identificador)', ('sim', 'nao'),
                                key=c)

        tipo_global[c] = st.selectbox('Selecione a tag',
                                      ['div', 'span', 'a', 'img', 'input', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                       'outro'],
                                      PRE_TAG[c], key = c)
        # nome_global = st.text_input("nome")

        # if tipo_global == 'outro:

        tipo_especifico[c] = st.selectbox('Selecione o identificador do elemento', ['class', 'id', 'outro'], key=c)

        nome_especifico[c] = st.text_input(" Nome do identificador usado", PRE_NOIDE[c])

        if unica[c] == 'nao':
            tagsMultiplas(URL, headers, tipo_global, tipo_especifico, nome_especifico, c)

        espaco()

    baixar = st.radio('Deseja baixar o arquivo .JSON?', ('nao', 'sim'))

    limpar = st.radio('Deseja forçar a deleção de "\ n" e "\ t"? ',  ('nao', 'sim'))

    minerar(URL, headers, unica, qntd_inputs, tipo_global, tipo_especifico, nome, nome_especifico, baixar, limpar)

    # y = st.radio('tag única? (Não há outras tags com o mesmo identificador)', ('sim', 'nao'))
    # if y == 'sim':
    #     print(session_state)
        # with open('data.txt', 'w') as outfile:
        #     json.dump(texto_formatado, outfile)


def tagsMultiplas(URL, headers, tGlobal, tEspecifico, nEspecifico, c):
    global cont
    cont += 1
    if st.button('Buscar tags', key=cont):
        try:
            page = requests.get(URL, headers=headers)
        except:
            print('Deu problema')

        soup = BeautifulSoup(page.text, 'html.parser')

        conjunto = soup.findAll(tGlobal[c], attrs={tEspecifico[c]: nEspecifico[c]})

        for item in conjunto:
            st.text(item.text)


def minerar(URL, headers, unc, qntd, tGlobal, tEspecifico, nome, nEspecifico, baixar, limpar):
    global x
    if st.button('Minerar'):
        page = requests.get(URL, headers=headers)
        # page.raise_for_status()

        ultimo_scrap['URL'] = URL
        ultimo_scrap['qntd_inputs'] = int(qntd)

        soup = BeautifulSoup(page.text, 'html.parser')

        texto = ''
        text = []
        x = {}

        # Salvar último scrap usado
        tag = []
        tEsp = []
        nEsp = []
        Nome = []

        for c in range(0, int(qntd)):
            # print(nEspecifico[c])
            text.clear()
            try:
                tag.append(tGlobal[c])
                tEsp.append(tEspecifico[c])
                nEsp.append(nEspecifico[c])
                Nome.append(nome[c])

                if unc[c] == 'sim':
                    texto = soup.find(tGlobal[c], attrs={tEspecifico[c]: nEspecifico[c]}).text

                    if limpar == 'sim':
                        x[nome[c]] = texto.strip().replace('\n', '').replace('\t', '')
                    else:
                        x[nome[c]] = texto.strip()
                else:
                    textos = soup.findAll(tGlobal[c], attrs={tEspecifico[c]: nEspecifico[c]})
                    for txt in textos:
                        # print(txt)
                        if limpar == 'sim':
                            text.append((txt.text).replace('\n', '').replace('\t', ''))
                        else:
                            text.append((txt.text))

                        print(text)

                    # textos.clear()
                    x[nome[c]] = text[:]

                    print(x)

                # print(text)

            except:
                texto = f" !!! ERRO !!! Input {c + 1} -> TAG/ID errada ou inexistente!"

                # text.append(texto)


        # for t in text:
            # st.text(t)

        ultimo_scrap['nome'] = Nome
        ultimo_scrap['TAG'] = tag
        ultimo_scrap['ident_elemento'] = tEsp
        ultimo_scrap['nome_ident'] = nEsp

        with open('ult_scrap.txt', 'w') as outfile:
            json.dump(ultimo_scrap, outfile)

        st.header('Scrap utilizado:')
        st.text(json.dumps(ultimo_scrap, indent=4))

        st.header('Resultado do Scrape:')
        texto_formatado = json.dumps(x, ensure_ascii=False).encode('utf8')
        st.text(json.dumps(x, indent=4))


        # session_state.texto = x

        if baixar == 'sim':
            for c in range(1, 200):
                if not os.path.isfile('scraps/scrap'+str(c)+'.json'):
                    with open('scraps/scrap'+str(c)+'.json', 'w') as outfile:
                        json.dump(x, outfile)
                    break

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }

    # page = requests.get("https://mises.org.br/article/3340/nos-150-anos-da-revolucao-marginalista-um-resumo-de-suas-cruciais-constatacoes", headers=headers)
    # https://webscraper.io/test-sites/e-commerce/allinone
    #

    # page.raise_for_status()
    #
    # soup = BeautifulSoup(page.text, 'html.parser')

    st.sidebar.title('Menu')
    selected = st.sidebar.selectbox('Selecione a página', ['Manual', 'Automatico', 'Carregar JSON'])

    if selected == 'Manual':
        metodoManual(headers)
    elif 'Carregar JSON':
        st.title('Carregamento de JSON')

        if st.button('teste'):
            with open('data.json') as json_file:
                data = json.load(json_file)
                print(data['Nome'])
                # print(json.dumps(data, indent=4))
    else:
        st.title('Webscraping Automatico')

    # start_date = datetime.date(1990, 7, 6)
    # date = st.date_input('Your birthday', start_date)

    # if date != start_date:
    #     field_1
    #     field_2
    #     date
main()
