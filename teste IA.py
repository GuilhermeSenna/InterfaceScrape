import csv
from collections import defaultdict
from itertools import islice, combinations
from copy import deepcopy

aux_regra = ''
regra = []
ultimo_nome = ''

def calcular_probabilidade(valor, total):
    return f'{(valor/total)*100:.2f}'


def mostrar_probabilidade(nomes, printar, ultimo):
    print(ultimo)
    global aux_regra, regra
    for x, n in enumerate(nomes):
        lista = []
        dicionario = {}
        total = 0

        for c in range(2):
            for nome in nomes[n]:
                total += 1
                if not lista:
                    lista.append(nome)
                if not nome in lista:
                    lista.append(nome)

                if c == 1:
                    for k in dicionario.keys():
                        if k == nome:
                            dicionario[k] += 1

            if c == 0:
                dicionario = dict.fromkeys(lista, 0)
                dicionario['total'] = total

        if printar:
            # print('-=' * 50)
            # print(n)
            for key, value in dicionario.items():
                # print(f'{key} -> {value}x, {calcular_probabilidade(value, dicionario["total"])}%')
                if x+1 == len(nomes):
                    if key != 'total' and int(float(calcular_probabilidade(value, dicionario["total"]))) == 100:
                        aux_regra += f' {key}'
                        regra.append(aux_regra)
                        aux_regra = ''


                    else:
                        aux_regra = ''
                else:
                    if key != 'total':
                        if aux_regra == '':
                            aux_regra = f'REGRA: {key} ->'
                        else:
                            aux_regra += f' {key} ->'

                # print(aux_regra)

                # if key != 'total' and int(float(calcular_probabilidade(value, dicionario["total"]))) == 100:
                #     print(f'Regra: {key} -> {value}')


def retirar_ocorrencias(nomes, variavel, valor):
    # Essa lógica permite remover todas as ocorrências que não forem a escolhida
    # Para poder criar uma lógica
    # print(nomes)
    indices = [i for i, x in enumerate(nomes[variavel]) if x != valor]

    for key, value in nomes.items():
        cont = 0
        for i in indices:
            nomes[key].pop(i - cont)
            cont += 1

    return nomes


filename = "lenses.csv"

# opening the file using "with"
# statement
nomes = None
keys_list = None
dates_dict = defaultdict(list)
with open(filename, 'r') as data:
    for key, line in enumerate(csv.reader(data)):
        # atributos = line[0].split(';')
        atributos = line[0].split(';')

        # Atribuindo as variaveis para o dicionário (Como nome, sexo, etc..)
        if key == 0:
            nomes = dict.fromkeys(atributos, '')
            keys_list = list(nomes)

        # Atribuindo os valores das variaveis no dicionário (Como sexo sendo 'M' e 'F')
        else:
            # Adicionando a uma lista auxiliar
            for x, y in enumerate(atributos):
                dates_dict[x].append(str(y).replace('"', ''))

            # Adicionando da lista auxiliar para o dicionário
            for x in dates_dict:
                nomes[f'{keys_list[x]}'] = dates_dict[x]

# 1º Passa o dicionário
# 2º Perguntar se quer printar ou não

# mostrar_probabilidade(nomes, False)

'''
for c in range(len(nomes)-2):
    comb = combinations(nomes, c+1)

    for i in list(comb):
        aux_nomes = deepcopy(nomes)
        for k in i:
            aux_nomes.pop(k, None)
        # print(aux_nomes)
        for i, nome in enumerate(aux_nomes):
            # print('=-'*20)
            # print(nome)
            mylist = list(set(aux_nomes[nome]))
            # print(mylist)
            for item in mylist:
                aux_nomes2 = deepcopy(aux_nomes)
                aux_nomes2 = retirar_ocorrencias(aux_nomes2, nome, item)
                mostrar_probabilidade(aux_nomes2, True)


            if i+1 == len(aux_nomes):
                break
'''

aux_nomes = deepcopy(nomes)
aux_nomes.pop('age', None)
for i, nome in enumerate(aux_nomes):
    mylist = list(set(aux_nomes[nome]))
    for item in mylist:
        aux_nomes2 = deepcopy(aux_nomes)
        aux_nomes2 = retirar_ocorrencias(aux_nomes2, nome, item)
        mostrar_probabilidade(aux_nomes2, True, item)



# Remover chave do dicionário pelo index
# del nomes[next(islice(nomes, 0, None))]


# for nome in nomes:
#     mylist = list(set(nomes[nome]))
#     for item in mylist:
#         aux_nomes = deepcopy(nomes)
#         aux_nomes = retirar_ocorrencias(aux_nomes, nome, item)
#         mostrar_probabilidade(aux_nomes, True)
#         # print(item)
#         # print(regra)
#
#     break

# print(nomes)
# nomes = retirar_ocorrencias(nomes, 'tear-prod-rate', 'reduced')

# mostrar_probabilidade(nomes, True)