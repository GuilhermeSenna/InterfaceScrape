import streamlit as st
import streamlit.components.v1 as stc


# Função usada para simular o <br> do HTML, ou seja, uma separação horizontal
def espaco():
    # st.text('-=' * 45)
    st.markdown('---')


# Função utilizada para mostrar um exemplo de como preencher os inputs
def exemplo():
    # st.info(''
    #         ' <p class="paragraph"> Paragrafo qualquer </p>\n\n'
    #         'tag: p\n'
    #         '\nidentificador usado: class\n\n'
    #         'Nome do identificador: paragraph')
    # st.markdown('')
    # st.markdown('')
    # st.markdown('')

    st.subheader("Exemplo de preenchimento dos inputs")
    st.markdown(
        f'<p style=" color: white;">&lt<span style="color: aquamarine;">p </span><span style="color: chartreuse;">'
        'class</span>="<span style="color: darkorchid;">paragraph</span>"&gt'
        ' Paragrafo qualquer &lt/<span style="color: aquamarine;">p</span>&gt</p>', unsafe_allow_html=True)

    # st.text('<p class="paragraph"> Paragrafo qualquer </p> ')
    st.markdown('**Tag:** <span style="color: aquamarine;">p </span>', unsafe_allow_html=True)
    st.markdown('**Identificador usado:** </span><span style="color: chartreuse;">class</span>', unsafe_allow_html=True)
    st.markdown('**Nome do identificador:** <span style="color: darkorchid;">paragraph</span>', unsafe_allow_html=True)
