import re

import streamlit as st
import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup
import SessionState
import os.path
from autoscraper import AutoScraper
import json

# lyrics += str(lyric).lower().replace('<p>', '').replace('</p>', '').replace('<br/>', ' ').replace('(', '').replace(')', '').replace(',', '') + ' '

# Variáveis auxiliares/globais
ultimo_scrap = {}
cont = 0
session_state = SessionState.get(texto='')
# URL_multiplas = []
unicidade = ''
QNTD = 0
LAST = 2
x = {}
text_save = []

# Constantes utilizadas para ser restaurado o último scrap
PRE_URL = ''
PRE_QNTD = 1
PRE_NOME = ['', '', '', '', '', '', '', '', '', '']
PRE_TAG = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
PRE_IDEEL = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
PRE_NOIDE = ['', '', '', '', '', '', '', '', '', '']


# Função usada para simular o <br> do HTML, ou seja, uma separação horizontal
def espaco():
    st.text('-=' * 45)


# Função utilizada para mostrar um exemplo de como preencher os inputs
def exemplo():
    st.subheader("Exemplo de preenchimento dos inputs")
    st.text('<p class="paragraph"> Paragrafo qualquer </p> ')
    st.text('tag: p')
    st.text('identificador usado: class')
    st.text('Nome do identificador: paragraph')


# Função que mostra o último scrape utilizado no topo da página
def ultimo_scrape():
    try:
        with open('ult_scrap.txt') as json_file:
            data = json.load(json_file)

        st.subheader("Último Scrap usado:")

        st.text(json.dumps(data, indent=4))

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
    global PRE_URL, PRE_QNTD, PRE_NOME, PRE_TAG, PRE_IDEEL, PRE_NOIDE

    PRE_URL = data['URL']
    PRE_QNTD = data['qntd_inputs']

    for k, v in enumerate(data['nome']):
        PRE_NOME[k] = v

    for k, v in enumerate(data['TAG']):
        PRE_TAG[k] = v
        PRE_TAG[k] = ['div', 'span', 'a', 'img', 'input', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i',
                      'outro'].index(PRE_TAG[k])

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


# Função principal de mineração
def minerar(URL, headers, unc, qntd, tGlobal, tEspecifico, nome, nEspecifico, baixar, limpar, URL_base, complemento, multiplas):
    global x, QNTD, LAST, text_save
    if st.button('Minerar', key=LAST) or multiplas:

        page = requests.get(URL, headers=headers)

        if page.status_code == 200:

            soup = BeautifulSoup(page.text, 'html.parser')

            # page.raise_for_status()

            ultimo_scrap['URL'] = URL

            ultimo_scrap['qntd_inputs'] = int(qntd)



            texto = ''
            text = []

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
                                text.append(txt.text.replace('\n', '').replace('\t', ''))
                            else:
                                text.append(txt.text)

                            # print(text)

                        # textos.clear()
                        if not multiplas:
                            x[nome[c]] = text[:]
                        else:
                            x[nome[c]] += text[:]

                    # print(text)

                except:
                    texto = f" !!! ERRO !!! Input {c + 1} -> TAG/ID errada ou inexistente!"

                    # text.append(texto)

            # for t in text:
            # st.text(t)

            # minerar(URL, headers, unc, qntd, tGlobal, tEspecifico, nome, nEspecifico, baixar, limpar)

            print(URL)

            QNTD = int(QNTD)

            while QNTD > 0:
                nova_url = f'\n{URL_base}{complemento}{LAST}'

                sleep(4)

                LAST += 1
                QNTD -= 1
                minerar(nova_url, headers, unc, qntd, tGlobal, tEspecifico, nome, nEspecifico, baixar, limpar, URL_base, complemento, True)

            if not multiplas or QNTD == 0:

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
                texto_indent_formatado = json.dumps(x, ensure_ascii=False, indent=4).encode('utf8')
                st.text(texto_indent_formatado.decode())

                # session_state.texto = x

                if baixar == 'sim':
                    for c in range(1, 200):
                        if not os.path.isfile('scraps/scrap' + str(c) + '_result.json'):
                            with open('scraps/scrap' + str(c) + '_config.json', 'w') as outfile:
                                json.dump(ultimo_scrap, outfile)
                            with open('scraps/scrap' + str(c) + '_result.json', 'w') as outfile:
                                json.dump(x, outfile)
                            break
            else:
                st.header('Ocorreu algum erro na solicitação.\n Código de resposta: ' + str(page.status_code))


# Função 'main'
def metodoManual(headers):
    global QNTD

    # Coloca o título na página
    st.title('Webscraping Manual')

    # Variável responsável por receber os dados do último scrape
    data = ultimo_scrape()

    # Escolher usar ou não o último scrape
    usar_ultimo(data)

    # URL/Link informada para scrape
    URL = st.text_input('URL do site', PRE_URL)

    # Quantidade de inputs a ser scrapeado
    qntd_inputs = st.text_input('Digite a quantidade de inputs (Por padrão é deixado 1)', PRE_QNTD)

    #
    # if qntd_inputs == '':
    #     qntd_inputs = 1

    # agrupamento = st.radio(' Qual a forma de agrupamento a ser usada?', ('Linear', 'Conjuntos', 'Mista'))

    espaco()

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
                st.text(f'\n{URL_base}{complemento}{c+2}')

    espaco()

    exemplo()

    espaco()

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
        unica[c] = st.radio('tag única? (Não há outras tags com o mesmo identificador)', ('sim', 'nao'),
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

        espaco()

    # Opcionalidades para o usuário
    baixar = st.radio('Deseja baixar o arquivo .JSON?', ('nao', 'sim'))
    limpar = st.radio('Deseja forçar a deleção de "\ n" e "\ t"? ', ('nao', 'sim'))

    # Função principal de mineração
    minerar(URL, headers, unica, qntd_inputs, tipo_global, tipo_especifico, nome, nome_especifico, baixar, limpar, URL_base, complemento, False)

    # y = st.radio('tag única? (Não há outras tags com o mesmo identificador)', ('sim', 'nao'))
    # if y == 'sim':
    #     print(session_state)
    # with open('data.txt', 'w') as outfile:
    #     json.dump(texto_formatado, outfile)


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', }

    st.sidebar.title('Menu')
    selected = st.sidebar.selectbox('Selecione a página', ['Manual', 'Automatico', 'Carregar JSON', 'Buscar exemplo'])

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
        st.title('Buscando exempo')

        link = st.text_input('URL')

        teste = st.text_input('Texto a ser buscado')

        if st.button('Buscar'):
            page = requests.get(link, headers=headers)

            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')

                if len(soup.findAll(text=re.compile(teste, re.IGNORECASE))) != 0:
                    for t in soup.findAll(text=re.compile(teste, re.IGNORECASE)):

                        espaco()

                        # st.text(t)

                        st.text(t.parent)

                        # st.text(t.parent.attrs)

                        i = t.parent.attrs

                        try:
                            # st.text(i['class'])

                            classe = ''

                            for x in i['class']:
                                classe += x
                                classe += ' '
                            classe.rstrip()

                            st.text(f'class = {classe}')
                        except:
                            pass



                    espaco()
                else:
                    st.text('Nada encontrado :(')
        pass
    # else:
    #     st.title('Webscraping Automatico')


# Início aqui
main()
