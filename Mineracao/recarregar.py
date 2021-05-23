
# Não funciona como deveria

# Função usada para perguntar para o usuário se ele quer usar ou não o último scrape
def usar_ultimo(data, PRE_URL, PRE_QNTD, PRE_NOME, PRE_TAG, PRE_IDEEL, PRE_NOIDE, PRE_UNICA, st):
    ult = st.radio('Usar último scrape?', ('nao', 'sim'))

    if ult == 'sim':
        recarregar(data, PRE_URL, PRE_QNTD, PRE_NOME, PRE_TAG, PRE_IDEEL, PRE_NOIDE, PRE_UNICA)


# Função utilizada para recarregar na página o último scrape utilizado
def recarregar(data, PRE_URL, PRE_QNTD, PRE_NOME, PRE_TAG, PRE_IDEEL, PRE_NOIDE, PRE_UNICA):

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

    return PRE_URL, PRE_QNTD, PRE_NOME, PRE_TAG, PRE_IDEEL, PRE_NOIDE, PRE_UNICA