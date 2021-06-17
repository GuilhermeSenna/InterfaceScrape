import csv
from collections import defaultdict
from itertools import islice, combinations, product
from copy import deepcopy
import time

aux_regra = ''
regra = []
ultimo_nome = ''


def symmetric_difference(a, b):
    return {*a} ^ {*b}


def calcular_probabilidade(valor, total):
    return f'{(valor/total)*100:.2f}'


def mostrar_probabilidade(nomes, printar):
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
                        checar = False
                        cont = 0

                        for i, r in enumerate(list(regra)):
                            if aux_regra in r:
                                checar = True
                                regra.pop(i - cont)
                                cont += 1

                        if not checar:
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

testes = []
inicio = time.time()
for n in range(len(nomes)-2): # Gera as combinações
    comb = combinations(nomes, n+1)
    for co in list(comb):  # Pega cada combinação em si
        aux_nomes = deepcopy(nomes)
        for c in co:
            aux_nomes.pop(c, None)
        for i, nome in enumerate(aux_nomes):
            mylist = list(set(aux_nomes[nome]))
        allNames = aux_nomes
        combinationes = product(*(aux_nomes[Name] for Name in allNames))

        combinacoes = list(set(list(combinationes)))

        # print(combinacoes)

        for com in combinacoes:
            aux_nomes2 = deepcopy(aux_nomes)

            # print(f'Deixando apenas {com}')
            for c_ in com:
                for nome in aux_nomes2:
                    if c_ in aux_nomes2[nome]:
                        # print(f'>>{c}')
                        # print(aux_nomes2)
                        aux_nomes2 = retirar_ocorrencias(aux_nomes2, nome, c_)
            # print(aux_nomes2)
            # print(f'Temos {aux_nomes2}\n\n')
            mostrar_probabilidade(aux_nomes2, True)
            # print(aux_nomes2)
            #
            # print(aux_nomes2)
            # print(c)

        regra = list(dict.fromkeys(regra))
        ss = list()
        for r in regra:
            # print(r)
            s = r.split(' -> ')
            s = [x.replace("REGRA: ", "") for x in s]
            ss.append(s)
            # aux_nomes2 = retirar_ocorrencias(aux_nomes2, nome, item)
            pass

        for s in ss:
            if not s in testes:
                testes.append(s)
                pass


fim = time.time()
print(f'{fim - inicio:.2f} segundos para gerar as regras.')


# print(nomes)

# nomes = retirar_ocorrencias(nomes, 'tear-prod-rate', 'reduced')

# mostrar_probabilidade(nomes, True)


# print(aux_nomes)


# nomes.pop('age', None)
# nomes.pop('prescrip', None)
# nomes.pop('astigmatism', None)
# nomes = retirar_ocorrencias(nomes, 'astigmatism', 'no')
# nomes = retirar_ocorrencias(nomes, 'tear-prod-rate', 'reduced')

# print('\n\n\n\n')
# mostrar_probabilidade(nomes, True)

# print(regra)

testes.sort(key=len)
items = []
items2 = []
for t, lista in enumerate(testes):
    if len(lista) == 2:
        regra.clear()

        aux_nomes = deepcopy(nomes)
        # Pega todas as keys do dicionário
        list_aux = []
        for nom in aux_nomes:
            list_aux.append(nom)

        # Deixa só as keys que não estão presentes
        for l in lista:
            for lx in list_aux:
                if l in aux_nomes[lx]:
                    list_aux.pop(list_aux.index(lx))

        # Retira do dicionário as keys que não estão presentes
        for lx in list_aux:
            aux_nomes.pop(lx, None)

        for k, v in aux_nomes.items():
            if lista[0] in v:
                aux_nomes = retirar_ocorrencias(aux_nomes, k, lista[0])
                break

        mostrar_probabilidade(aux_nomes, True)
        if not regra:
            items.append(lista)
    else:
        # Roda apenas uma vez após a seleção das regras
        if items:
            for i in items:
                testes.pop(testes.index(i))
            items.clear()


ls = ['reduced', 'none']
ls2 = ['no', 'reduced', 'none']

print(ls in ls2)
# for t, lista in enumerate(testes):
#     if lista == ls or ls not in lista:


print(testes)


# print(aux_nomes)
    # for item in mylist:
    #     aux_nomes2 = deepcopy(aux_nomes)
    #     aux_nomes2 = retirar_ocorrencias(aux_nomes2, nome, item)
    #     mostrar_probabilidade(aux_nomes2, True, item)





"""

regra = list(dict.fromkeys(regra))
ss = list()
for r in regra:
    # print(r)
    s = r.split(' -> ')
    s = [x.replace("REGRA: ", "") for x in s]
    ss.append(s)
    # aux_nomes2 = retirar_ocorrencias(aux_nomes2, nome, item)
    pass

for s in ss:
    # print(s)
    pass

# indices = []
#
# for k, v in enumerate(ss):
#     for x, y in enumerate(ss):
#         if len(list(set(v) - set(y))) == 2:
#             ss.pop(ss.index(v))
#             ss.pop(ss.index(y))
#             break
#
#
#
# print(ss)

# print(list(combinations))

# prod = list(product(*list_of_list))
# for pr in prod:
#     aux_regra = ''
#     aux_nomes2 = deepcopy(aux_nomes)
#     for p in pr:
#         aux_nomes2 = retirar_ocorrencias(aux_nomes2, nome, item)

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

"""