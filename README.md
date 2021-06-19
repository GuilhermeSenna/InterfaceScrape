# InterfaceScrape

## Repositório alterado para público em 18/06/2021

**Projeto pessoal feito com a biblioteca/Framework Streamlit usada para criar a interface WEB**
 
 ![Streamlit Logo](Streamlit_Logo_1.jpg)

---

# index.py

## Opção "Manual":

> Programa principal do repositório
- Usado para fazer webcrape dinamicamente 
- Salva a última configuração de scrap usada ou qualquer outra que o usuário queira
- Salva também o resultado do scrap, para uso futuro
  - Ambos acima com JSON
- Possui exemplo didático para o usuário entender como funcionam os inputs
- Inputs gerados dinamicamente de acordo com a escolha do usuário (max 10, por enquanto)
- Permite destrinchar tags múltiplas para pegar a desejada
- Opção de deletar quebras de linha ou espaço para melhor resultado (Beta)

**O que falta?**

- Lógica para múltiplas em sequência e múltiplas avulsas
- Adaptar para diferentes situações (Site de notícias, economia, etc..)


## Opção "Carregar JSON":

> Programa complementar
> Utilizado para uso prático do resultado do scrap do programa principal
- Por enquanto gera tabela a partir de JSON
- Falta elaborar mais

## Opção "Buscar exemplo"

> Programa complementar
> Focado em sites de notícia
> A ideia é obter todo o conteúdo da notícia a partir de um fragmento da mesma
- Possui um slider para selecionar a generalização
  - Isso permite que se obtenha o conteúdo de diferentes sites com diferentes formas de dispor o texto no site
- Lida com problemas no site de UTF-8
- O usuário pode tentar algumas opções de corrigir alguns problemas de formatação (não resolve todos)

**O que falta?**

- Lidar com acentuação/codificação UTF-8
  - Foi tentado uma lógica similar mas o resultado retornaria o texto sem acentuação
- Alguns sites barram por detectar o bot, retornam textos ilegíveis (Não é por conta de UTF-8)
- Alguns sites geram muitos resíduos (textos em imagens, links de anúncio)
 
---

# Projeto iniciado em 18/05/2021 mas já idealizado anteriormente

## Todas as mudanças por ordem cronológica:

**18/05/2021**
- Adição do SessionState.py usado para guardar o estado atual (variáveis globais)
- Cria arquivo.JSON
- Opcionalidade pro usuário baixar ou não JSON, remover forçado ou n os \n e \t
- Nova janela para Carregamento do JSON


**19/05/2021**

- Projeto Comentado
- Corrigido erro de duplicação widget
- Tag <i> adicionada
- Correções no encode/decode UTF8
- Config do IMDB e Amazon Salvas
- Lógica de multipáginas iniciada (falta mais testes)
- Lógica feita para manter os valores antigos ao passar de páginas

**20/05/2021 - 21/05/2021**

Nova janela pra buscar elementos pelo conteúdo
- Janela criada
- Lógica para buscar elemento (burlando case sensitive)
- Acha a tag pai e seus atributos

**21/05/2021 - 22/05/2021**

Evolução em buscar elementos pelo conteúdo
- Lógica para guardar e checar se o último link buscado é o mesmo do último usado
> Isso evita de fazer outra requisição, evitando de o IP ser banido e também busca mais rapidamente
- Revisão na lib - Soup Beatiful
- Coleta elementos de tag iguais dinamicamente (falta polir)
- Busca tag mais exterior (falta procurar exemplos para tags ainda mais englobadas)
- Buscar exemplo de função para package

Minerar Manual
- Tag de unicidade adicionada no JSON

**22/05/2021 - 23/05/2021**

Modularização, novas lógicas e novos layouts

- Minerar, Exemplo e Espaco migrados para um package
- Tentativa de colocar o funcionamento de recarregar em um package mal sucedido
- Corrigido erro de DuplicateWidgetID no buscar texto
- Iniciado lógica para separar elementos de uma div com muitos elementos {feita em parte}
- Iniciado lógica para carregar scraps salvos (sem se restringir apenas ao último) -> Por enquanto só lista
- Aparecendo itens que estão dentro de uma tag, com a possibilidade de escolher quais quer manter
> possibilidade de selecionar tudo e remover aos poucos.

Layout:
- Dropdown para mostrar o último scrap
- Exemplo melhorado (negrito)
- Elemento próprio para JSON utilizado
- Quantidade de inputs alterado para number.value


**23/05/2021**

FrontEnd
- Adaptação de Radio para Checkbox aonde necessário
- Mensagem avisando que está carregando ao buscar múltiplas páginas
- Adicionando Título e deixando o layout wide como padrão
- Mensagem de erro estilizada
- Streamlit.components importado + testes com HTML
- Exemplo melhorado/estilizado

BackEnd
- Opção de escolher último scrap inserido na lista de scraps
- Correção cast bool() não converte corretamente a string
- Carregamento de JSON concluído com sucesso tanto as config quanto results
- Agora todos os arquivos salvos são em JSON (Faltava o último)

Front + Back
- Carregar JSON continuado
- Carrega arquivos
- Gera tabela (ainda não está 100%)


**26/05/2021**
- Ignora retorno ruins ao puxar texto, puxando vazio ou None, facilita ao escolher itens ruins
- Falta retirar resíduos
- Correção em encodificação/decodificação UTF-8, vindo quebrada
- printa texto formatado
- Adicionado Strip() para corrigir textos com espaços longos
- Corrigido erro de DuplicateWidgetID caso seja escolhido 2 tags pais diferentes
- Feito testes em diversos sites, funcionando bem ou parcialmente na maioria

**28/05/2021**
- Buscar exemplo agora é flexível o nível de generalização em que buscará as tags similares
> Dessa forma sites que deixam textos separados em blocos podem ser obtidos os textos completos
- "Mostrar tag pai" alterado para checkbox
- Mostra tag filho e pai
- Nova checkbox para tags dividida em partes
- Adicionado para escolher itens ruins em tags agrupadas
- Nova opção extra junto da divisão em partes, para separar em paragrafos (não está 100% ainda)

## Demais mudanças podem ser checadas nos commits.
