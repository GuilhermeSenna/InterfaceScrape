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
    st.title('Buscando exempo')

    link = st.text_input('URL')

    teste = st.text_input('Texto a ser buscado')

    select_slider = st.slider('Nível de generalização', 0, 10)

    if st.button('Buscar') or session_state.last_URL == link:

        # st.text(select_slider)

        # Checando se o último request do usuário foi feito usando o mesmo Link
        if session_state.last_URL != link:
            session_state.last_URL = link
            session_state.req = page = requests.get(link, headers=headers)
        else:
            page = session_state.req

        if page.status_code == 200:
            # unicodedata.normalize('NFKD', page.text).encode('ascii', 'ignore').decode('utf8')
            soup = BeautifulSoup(fix_encoding(page.text), 'html.parser')

            if len(soup.findAll(text=re.compile(teste, re.IGNORECASE))) != 0:
                for v, t in enumerate(soup.findAll(text=re.compile(teste, re.UNICODE))):

                    st.markdown('---')

                    # st.text(t)

                    # st.text(t.parent)
                    #
                    # TAG
                    # st.text(t.parent.name)

                    st.text(f'Filho: {t}')

                    mostrar_pai = st.checkbox('Mostrar tag pai?', key=v)

                    if mostrar_pai:
                        # st.text(t.parent.parent)

                        x = t
                        for c in range(select_slider):
                            x = x.parent

                        gerar_textos(x, v)

                    try:

                        tag = x.name

                        i = x.attrs
                        # st.text(i['class'])

                        classe = ''

                        for x in i['class']:
                            classe += x
                            classe += ' '
                        st.text(f'class = {classe}')
                        classe = classe.strip()

                        if st.button('Buscar outros com essa class'):
                            soup = BeautifulSoup(page.text, 'html.parser')
                            tst = soup.find(tag, attrs={'class': classe})
                            st.text(tst.strings[0])
                    except:
                        pass

                st.markdown('---')
            else:
                st.error('Nada encontrado :(')
    pass
