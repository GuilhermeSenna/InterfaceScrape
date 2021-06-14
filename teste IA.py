import csv
from collections import defaultdict


def calcular_probabilidade(valor, total):
    return f'{(valor/total)*100:.2f}'


def mostrar_probabilidade(nomes, printar):
    for n in nomes:
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
            print('-=' * 50)
            print(n)
            for key, value in dicionario.items():
                print(f'{key} -> {value}x, {calcular_probabilidade(value, dicionario["total"])}%')


def retirar_ocorrencias(nomes, variavel, valor):
    # Essa lógica permite remover todas as ocorrências que não forem a escolhida
    # Para poder criar uma lógica
    indices = [i for i, x in enumerate(nomes[variavel]) if x != valor]

    for key, value in nomes.items():
        cont = 0
        for i in indices:
            nomes[key].pop(i - cont)
            cont += 1

    return nomes


filename = "student-mat.csv"

# opening the file using "with"
# statement
nomes = None
keys_list = None
dates_dict = defaultdict(list)
with open(filename, 'r') as data:
    for key, line in enumerate(csv.reader(data)):
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
mostrar_probabilidade(nomes, False)

mostrar_probabilidade(nomes, True)