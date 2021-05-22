import requests
from bs4 import BeautifulSoup
import re


def espaco(st):
    st.text('-=' * 45)


def buscar_exemplo(headers, st, session_state):
    st.title('Buscando exempo')

    link = st.text_input('URL')

    teste = st.text_input('Texto a ser buscado')

    if st.button('Buscar') or session_state.last_URL == link:

        # Checando se o último request do usuário foi feito usando o mesmo Link
        if session_state.last_URL != link:
            session_state.last_URL = link
            session_state.req = page = requests.get(link, headers=headers)
        else:
            page = session_state.req

        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')

            if len(soup.findAll(text=re.compile(teste, re.IGNORECASE))) != 0:
                for t in soup.findAll(text=re.compile(teste, re.IGNORECASE)):

                    espaco(st)

                    # st.text(t)

                    st.text(t.parent)

                    st.text(t.parent.name)

                    mostrar_pai = st.radio('Mostrar tag pai?', ['nao', 'sim'])

                    if mostrar_pai == 'sim':
                        st.text(t.parent.parent)

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

                espaco(st)
            else:
                st.text('Nada encontrado :(')
    pass