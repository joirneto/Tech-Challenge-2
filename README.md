# POS FIAP ALURA - IA PARA DEVS
## Tech Challenge Fase 2
### Integrantes Grupo 26

- André Philipe Oliveira de Andrade(RM357002) - andrepoandrade@gmail.com
- Joir Neto (RM356391) - joirneto@gmail.com
- Marcos Jen San Hsie(RM357422) - marcosjsh@gmail.com
- Michael dos Santos Silva(RM357009) - michael.shel96@gmail.com
- Sonival dos Santos(RM356905) - sonival.santos@gmail.com

Video(Youtube): 

## Descrição do Problema: Vehicle Routing Problem

O **Vehicle Routing Problem** (VRP) é um problema clássico de otimização de rotas, muito comum no setor de logística e distribuição, que pode ser resolvido com o uso de algoritmos genéticos. O problema consiste em otimizar as rotas que uma frota de veículos deve seguir para atender a demanda de uma lista de clientes, respeitando restrições como a capacidade dos veículos e, em alguns casos, janelas de tempo específicas para entrega.

Neste projeto, utilizamos tanto um algoritmo genético quanto um algoritmo convencional para propor uma solução a um caso fictício envolvendo a **Bem-Te-Vi Logística** e a **CasaBella Pisos e Revestimentos**.

O objetivo principal é minimizar o custo logístico, reduzindo a distância percorrida pelos veículos, sem ultrapassar os limites de carga, garantindo que todos os clientes sejam atendidos. Além disso, realizaremos uma comparação entre as soluções apresentadas pelos dois algoritmos.

### Situação Problema:

A **Bem-Te-Vi Logística** é uma empresa contratada para atender exclusivamente a fábrica **CasaBella Pisos e Revestimentos**. Com o lema de "entrega rápida e preço baixo", a empresa precisa otimizar o uso de sua frota de caminhões para realizar as entregas dos lotes produzidos pela fábrica, atendendo clientes em diversas localizações. Cada cliente solicita uma quantidade de produtos, e cada caminhão possui uma capacidade máxima de carga que não pode ser excedida, por razões de segurança.

### Premissas e Restrições:
- Cada cliente possui uma localização (coordenadas geográficas).
- Cada cliente tem uma demanda específica de produtos.
- Frota limitada de caminhões, com uma capacidade máxima de carga.
- As rotas devem começar e terminar no centro de distribuição da empresa.

### Parâmetros do Problema:
- Número de clientes: 15
- Capacidade de carga dos caminhões: 100 lotes por veículo
- Matriz de distâncias: Distâncias entre o depósito, os clientes e entre os próprios clientes.
- Demandas: Cada cliente tem uma demanda entre 5 e 20 lotes.

O desafio é criar rotas que respeitem a capacidade de carga e minimizem a distância total percorrida.

## Algoritmo Genético

O algoritmo genético, inspirado na evolução natural, busca "evoluir" uma solução ao longo de várias gerações. Ele começa criando várias soluções (uma "população"), seleciona as melhores, combina-as (crossover) e aplica mutações para encontrar soluções mais eficientes.

Neste projeto, utilizamos operadores genéticos como seleção por torneio, elitismo, crossover ordenado (OX), mutação adaptativa e um critério de parada baseado em melhoria de gerações.

## Algoritmo Convencional (Método Guloso)

O algoritmo guloso é uma abordagem direta, onde as decisões são tomadas com base nas informações locais, selecionando sempre o cliente mais próximo que possa ser atendido sem exceder a capacidade do caminhão. É uma solução rápida, mas que pode ficar presa em mínimos locais.

## Implementação dos Algoritmos

### 1. População Inicial:

Utilizamos duas abordagens para criar a população inicial do algoritmo genético: uma aleatória e outra heurística, com o uso do algoritmo KNN (k-vizinhos mais próximos).

#### Método Aleatório
As rotas são geradas embaralhando a ordem dos clientes, garantindo diversidade na população inicial, crucial para evitar que o AG caia em mínimos locais.

#### Método KNN
Aqui, utilizamos o algoritmo dos k-vizinhos mais próximos para criar uma população inicial.

O KNN tenta construir rotas iniciais razoáveis, baseadas nas distâncias entre clientes próximos. Isso é vantajoso porque evita que o algoritmo comece com rotas completamente aleatórias, o que pode retardar a convergência.

Utilizamos o KNN para criar rotas iniciais com base na proximidade geográfica entre os clientes, gerando rotas mais "razoáveis" desde o início. Após testes, encontramos a melhor convergência com `n_neighbors = 5`.

### 2. Avaliação (Fitness):

A função `calculate_distance` é usada para calcular a distância total percorrida por cada rota. No AG, o fitness de cada indivíduo (solução) é a distância total da rota, com soluções melhores tendo distâncias menores.

- Por quê? A função fitness é essencial para guiar o processo de seleção e reprodução. No VRP, minimizar a distância total é o objetivo principal, então a função fitness diretamente reflete a qualidade de uma solução.

### 3. Seleção por Torneio:

Torneio: Uma técnica de seleção que escolhe um subconjunto de indivíduos da população (o torneio) e seleciona o melhor dentro desse grupo para avançar para a próxima geração.
- Por quê? A seleção por torneio garante que as melhores soluções tenham uma maior chance de reprodução, mas ainda mantém um grau de diversidade, pois soluções menos ótimas ainda podem ser selecionadas.

### 4. Crossover Ordenado (OX):

Ordered Crossover (OX): O crossover é inspirado na reprodução biológica, combinando duas soluções (pais) para gerar novas (filhos). O OX preserva a ordem relativa dos elementos dos pais. Isso é crucial para o VRP, pois mudar drasticamente a ordem dos clientes em uma rota pode resultar em soluções inviáveis ou muito ineficientes.
- Por quê? O OX é uma técnica eficiente para problemas onde a ordem dos elementos (clientes) importa, garantindo que os filhos mantenham uma estrutura de rota similar aos pais, mas com variações que podem ser benéficas.

### 5. Mutação Adaptativa:

A mutação altera dois clientes de posição aleatoriamente em uma rota. A taxa de mutação decresce ao longo do tempo, começando alta para garantir diversidade e, gradualmente, diminuindo para explorar mais soluções próximas à melhor solução encontrada.
- Por quê? No início, mutações são importantes para explorar o espaço de busca. À medida que o algoritmo converge, a mutação é reduzida para evitar que soluções boas sejam destruídas e para focar no refinamento das melhores soluções.

### 6. Elitismo:

O melhor indivíduo (rota com menor distância) é sempre mantido para a próxima geração. Isso garante que a qualidade das soluções nunca piora de uma geração para outra.
- Por quê? O elitismo garante que a melhor solução encontrada até o momento não seja perdida, evitando que o AG perca a solução ótima ao longo das gerações.

### 7. Critério de Parada:

O algoritmo pára se não houver melhoria após um número predeterminado de gerações (`no_improvement_limit`), indicando que a solução não está mais melhorando.
- Por quê? Definir um limite de gerações sem melhoria ajuda a evitar que o algoritmo fique preso em loops desnecessários após convergir.

### Abordagem Gulosa:

O algoritmo guloso cria rotas cliente por cliente, sempre escolhendo o cliente mais próximo que ainda pode ser atendido sem exceder a capacidade do veículo. A abordagem gulosa é mais rápida, mas tende a ficar presa em mínimos locais, pois sempre toma a melhor decisão imediata, sem considerar o impacto a longo prazo.

## Visualização

A visualização com Pygame permite observar as rotas geradas, ajudando a entender como as soluções evoluem e como o algoritmo otimiza as rotas ao longo do tempo. Além de ser uma ferramenta de validação visual, é útil para explicar a convergência e o comportamento do AG.

## Considerações Finais

Por fim, com esta simulação, podemos comparar a eficiência dos algoritmos genéticos (População inicial aleatória e com knn) e do guloso aplicado ao VRP (Vehicle Routing Problem).

Inicialmente o guloso performou mais rápido e melhor em comparação ao genético com população inicial aleatória e crossover, sendo gerado por 5k gerações. Partindo desse ponto de comparação, inserimos:
- Mutação adaptativa: Crucial para ajustar a exploração e exploração ao longo do tempo, evitando a estagnação do algoritmo.
- Elitismo e torneio: Técnicas que garantem um equilíbrio entre exploração (diversidade) e exploração das melhores soluções.
- 10 interações para cada genético, com 3k gerações por interação.
- Critério de parada de 1k gerações sem melhoria.
Com essas melhorias o genético começou a performar melhor, encontrando soluções mais otimizada comparada com o guloso.

Na sequência das melhorias, realizamos uma abordagem heurística para a criação da população inicial do genético baseada no KNN. Assim encontrando a melhor solução convergindo entre a 1500ª e 2000ª geração, para o contexto em questão:

### Melhor Solução
- Rota: [4, 9, 7, 12, 10, 11, 14, 3, 1, 6, 5, 13, 8, 2, 15]
- Sub-rotas:
  - [0, 4, 9, 7, 12, 10, 11, 14, 3, 0]
  - [0, 1, 6, 5, 13, 8, 2, 15, 0]
  - (0 representa o depósito)
- Distância total: 368

Concluímos que:
- Algoritmo guloso: Simples e rápido, mas geralmente fornece uma solução subótima.
- AG com população inicial aleatória: Explora um espaço de soluções mais diverso, o que pode ajudar a evitar mínimos locais, mas tende a convergir mais lentamente.
- AG com população inicial baseada no KNN: Tendência a convergir mais rapidamente, devido à qualidade inicial da população. E foi quem estabeleceu dentre todas o melhor resultado (menor distância) considerando as demandas de cada cliente e capacidade do veículo.

OBS: Incluímos uma flag em nosso algoritmo `actived_best_value` caso desejem utilizar a melhor solução encontrada durante esses testes como valor inicial de uma nova bateria de testes. Basta setar a flag para `True`.

![Descrição da Imagem](./data/Melhor%20Resultado.jpg)
