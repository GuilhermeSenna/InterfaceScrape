import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import os

# Função principal de mineração
def minerar(URL, headers, unc, qntd, tGlobal, tEspecifico, nome, nEspecifico, baixar, limpar, URL_base, complemento, multiplas, st, ultimo_scrap, LAST, x, QNTD, text_save):
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
            unica = []

            for c in range(0, int(qntd)):
                # print(nEspecifico[c])
                text.clear()
                try:
                    tag.append(tGlobal[c])
                    tEsp.append(tEspecifico[c])
                    nEsp.append(nEspecifico[c])
                    Nome.append(nome[c])
                    unica.append(unc[c])

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
                ultimo_scrap['unica'] = unica

                with open('ult_scrap.txt', 'w') as outfile:
                    json.dump(ultimo_scrap, outfile)

                st.header('Scrap utilizado:')
                st.text(json.dumps(ultimo_scrap, indent=4))

                st.header('Resultado do Scrape:')
                texto_formatado = json.dumps(x, ensure_ascii=False).encode('utf8')
                texto_indent_formatado = json.dumps(x, ensure_ascii=False, indent=4).encode('utf8')
                st.json(texto_indent_formatado.decode())

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