import requests
from bs4 import BeautifulSoup
import re
import streamlit as st
from ftfy import fix_encoding
import unicodedata


# def espaco():
#     st.text('-=' * 45)


def gerar_textos(t, v):
    filhos = []
    filhotes = ['']
    filhotinhos = ['']
    testando = []
    # Limpando as string obtidas, que retorna vazio o none

    # st.text(t)

    englobado = st.checkbox('Selecione se está dividido em partes (provavelmente gerará mais resíduos)', key=v)

    if englobado:
        separar = st.checkbox('Tentar separar os paragráfos (pode ajudar ou piorar)', key=v)

    if englobado:

        testers = ''
        checar = False
        for tst in t.strings:
            if tst.strip():
                testando.append(tst.strip())
                checar = False
                if separar:
                    filhotes[len(filhotes)-1] += f'{tst.strip()} '
                    # filhos.append(f'{tst.strip()} ')
                else:
                    filhotes.append(tst.strip())
            else:
                if not checar:
                    filhotes.append('\n\n')
                    # filhos.append('\n\n')
                    checar = True

        container = st.beta_container()
        all = st.checkbox("Select all", key=v)


        if not separar:
            if all:
                selected_options = container.multiselect("Selecione uma ou mais opções:",
                                                         filhotes, filhotes, key=v)
            else:
                selected_options = container.multiselect("Selecione uma ou mais opções:",
                                                         filhotes, key=v)
        else:
            if all:
                selected_options = container.multiselect("Selecione uma ou mais opções:",
                                                         testando, testando, key=v)
            else:
                selected_options = container.multiselect("Selecione uma ou mais opções:",
                                                         testando, key=v)

        tester = ''
        if st.button('Printar', key=v):
            for t in selected_options:
                # HTML pra usar depois talvez como PDF
                # print(t)
                if not separar:
                    filhotinhos[len(filhotinhos)-1] += f'{t}'
                else:
                    tester += f'{t.strip()}\n\n'

            st.markdown('---')
            if not separar:
                for x in filhotinhos:
                    st.write(x)
            else:
                st.write(tester)
            st.markdown('---')
            # print(tester)

        try:
            st.text(f'> Pai:\nTag: {t.name}\nAtributos:{t.attrs}')
        except:
            pass

        st.markdown('---')
    else:
        try:
            for tste in t:
                if str(tste.string).strip() and tste.string is not None:
                    filhos.append(tste)
                    # print(tste)

            container = st.beta_container()
            all = st.checkbox("Select all", key=v)

            if all:
                selected_options = container.multiselect("Selecione uma ou mais opções:",
                                                         filhos, filhos, key=v)
            else:
                selected_options = container.multiselect("Selecione uma ou mais opções:",
                                                         filhos, key=v)

            tester = ''
            if st.button('Printar', key=v):
                for t in selected_options:
                    # HTML pra usar depois talvez como PDF
                    # print(t)
                    tester += f'{t.string.strip()}\n\n'

                st.markdown('---')
                st.write(f'{tester}')
                st.markdown('---')
                # print(tester)

            st.text(f'> Pai:\nTag: {t.name}\nAtributos:{t.attrs}')
        except AttributeError:
            st.error("Tente aumentar o nível de generalização")


def buscar_exemplo(headers, session_state):

    # Título para a página
    st.title('Buscando exempo')

    # Link/URL para a página a ser scrapeada
    link = st.text_input('URL')

    # Texto a ser buscado na página
    texto = st.text_input('Texto a ser buscado')

    # Slider para ser escolhido o nível de generalização
    select_slider = st.slider('Nível de generalização', 0, 10)

    # Caso clique no botão de buscar ou o último link digitado for igual ao atual
    # Checa se é igual ao atual para não fazer a mesma requisição novamente
    # Pois está fica salva
    if st.button('Buscar') or session_state.last_URL == link:

        # Checando se o último request do usuário foi feito usando o mesmo Link
        if session_state.last_URL != link:
            session_state.last_URL = link

            # Caso não seja ela salva no session para checar posteriormente
            session_state.req = page = requests.get(link, headers=headers)
        else:
            page = session_state.req

        # Caso o código da requisição seja 200
        if page.status_code == 200:

            # Lógica tentada para checagem com acentuação
            # unicodedata.normalize('NFKD', page.text).encode('ascii', 'ignore').decode('utf8')

            # Correção para possíveis problemas com UTF-8
            soup = BeautifulSoup(fix_encoding(page.text), 'html.parser')

            # Checa se achou algum texto na página com o texto informado a procurar
            # O re.compile e o re.IGNORECASE servem para ignorar Case Sensitive
            if len(soup.findAll(text=re.compile(texto, re.IGNORECASE))) != 0:

                # v = Usada para colocar no ID dos widgets, evitando erro de duplicação
                # t = Texto achado
                # UNICODE é para ter uma lógica parecida da anterior
                for v, t in enumerate(soup.findAll(text=re.compile(texto, re.UNICODE))):

                    # Linha horizontal
                    st.markdown('---')

                    # Mostra o filho
                    st.text(f'Filho: {t}')

                    # Pergunta se quer mostrar a tag pai
                    mostrar_pai = st.checkbox('Mostrar tag pai?', key=v)

                    # Caso queira mostrar a tag pai
                    if mostrar_pai:

                        # Vai indo pra tag mais externa dependendo do valor do slider (generalização)
                        for c in range(select_slider):
                            t = t.parent

                        # Função principal para gerar textos
                        gerar_textos(t, v)

                    try:

                        # Captura o nome da tag atual
                        tag = t.name

                        # Captura os atributos daquela tag, como class e ID
                        i = t.attrs

                        # Vai usar a classe porque ID não se repete
                        # coloca a variável para receber a(s) classe(s)
                        classe = ''

                        # Lógica para armazena se houver mais de uma classe na tag
                        for x in i['class']:
                            classe += x
                            classe += ' '

                        # Printa a classe completa
                        st.text(f'class = {classe}')

                        # Método strip() na classe
                        classe = classe.strip()

                        # Tenta buscar outros elementos com a mesma classe (não funcional)
                        if st.button('Buscar outros com essa class'):
                            soup = BeautifulSoup(page.text, 'html.parser')
                            tst = soup.find(tag, attrs={'class': classe})
                            st.text(tst.strings[0])
                    except:
                        pass

                # Linha horizontal
                st.markdown('---')
            else:

                # Mensagem de erro caso não ache nenhuma informação sobre o texto buscado
                st.error('Nada encontrado :(')