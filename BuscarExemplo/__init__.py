import requests
from bs4 import BeautifulSoup
import re
import streamlit as st
import unicodedata


def espaco():
    st.text('-=' * 45)


def buscar_exemplo(headers, session_state):
    st.title('Buscando exempo')

    link = st.text_input('URL')

    teste = st.text_input('Texto a ser buscado')

    filhos = []

    if st.button('Buscar') or session_state.last_URL == link:

        # Checando se o último request do usuário foi feito usando o mesmo Link
        if session_state.last_URL != link:
            session_state.last_URL = link
            session_state.req = page = requests.get(link, headers=headers)
        else:
            page = session_state.req

        if page.status_code == 200:
            # unicodedata.normalize('NFKD', page.text).encode('ascii', 'ignore').decode('utf8')
            soup = BeautifulSoup(page.text, 'html.parser')

            if len(soup.findAll(text=re.compile(teste, re.IGNORECASE))) != 0:
                for v, t in enumerate(soup.findAll(text=re.compile(teste, re.UNICODE))):

                    espaco()

                    # st.text(t)

                    st.text(t.parent)

                    # TAG
                    st.text(t.parent.name)

                    mostrar_pai = st.radio('Mostrar tag pai?', ['nao', 'sim'], key=v)

                    if mostrar_pai == 'sim':
                        # st.text(t.parent.parent)

                        for tste in t.parent.parent:
                            filhos.append(tste)

                        container = st.beta_container()
                        all = st.checkbox("Select all", key=v)

                        if all:
                            selected_options = container.multiselect("Selecione uma ou mais opções:",
                                                                     filhos, filhos, key=v)
                        else:
                            selected_options = container.multiselect("Selecione uma ou mais opções:",
                                                                     filhos, key=v)

                        # st.text(t.parent.parent.text)
                        # for t in t.parent.parent.findAll('p'):
                        #     print(t)
                        #     st.text(f'{t.text}\n')
                        #     st.text(f'{t.text}\n')

                    st.text(f'> Pai:\nTag: {t.parent.parent.name}\nAtributos:{t.parent.parent.attrs}')

                    tag = t.parent.name

                    # st.text(t.parent.attrs)

                    i = t.parent.attrs

                    # st.text(t.next_sibling)

                    try:
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

                espaco()
            else:
                st.error('Nada encontrado :(')
    pass