# Função usada para simular o <br> do HTML, ou seja, uma separação horizontal
def espaco(st):
    st.text('-=' * 45)


# Função utilizada para mostrar um exemplo de como preencher os inputs
def exemplo(st):
    st.subheader("Exemplo de preenchimento dos inputs")
    st.text('<p class="paragraph"> Paragrafo qualquer </p> ')
    st.markdown('**tag:** p')
    st.markdown('**identificador usado:** class')
    st.markdown('**Nome do identificador:** paragraph')
