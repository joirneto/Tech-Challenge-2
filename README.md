# POS FIAP ALURA - IA PARA DEVS
## Tech Challenge Fase 2
### Integrantes Grupo 26

- André Philipe Oliveira de Andrade(RM357002) - andrepoandrade@gmail.com
- Joir Neto (RM356391) - joirneto@gmail.com
- Marcos Jen San Hsie(RM357422) - marcosjsh@gmail.com
- Michael dos Santos Silva(RM357009) - michael.shel96@gmail.com
- Sonival dos Santos(RM356905) - sonival.santos@gmail.com

Video(Youtube): 

## Descrição do problema: Vehicle Routing Problem

Vehicle Routing Problem ou VRP é um problema de otimização de rotas comum no setor de logística e distribuição que pode ser resolvido com o uso de algoritmos genéticos. Este problema se baseia na otimização de rotas que uma frota de veículos pode seguir para atender as demandas de entrega de uma lista de clientes, considerando algumas restrições como a capacidade dos veículos e em alguns casos específicos, janelas de tempo específicas para entrega.

Neste projeto, faremos o uso de um algoritmo genético e um algoritmo convencional para elaborar uma solução para o caso fictício da Bem-Te-Vi Logística e da CasaBella Pisos e Revestimentos.

O objetivo é minimizar o custo logístico através da diminuição da distância percorrida pelos veículos, mantendo a segurança ao não ultrapassar os limites de carga, garantindo com que todos os clientes sejam atendidos. Também realizaremos comparativo das soluções apresentadas entre o algoritmo genético e o convêncional.

### Situação problema:

A Bem-Te-Vi Logística é uma empresa de logística contratada para atender exclusivamente a fábrica de materiais de construção CasaBella Pisos e Revestimentos. Com o lema de "entrega rápida e preço baixo", a empresa deve otimizar o uso de sua pequena frota de caminhões, a fim de realizar as entregas dos lotes produzidos pela fábrica a diversos clientes distribuídos em diferentes localizações geográficas. Cada um destes clientes, realiza a encomenda de uma quantidade de produtos e cada caminhão tem uma capacidade máxima de carga que não pode ser excedida por questões de segurança.

### Premissas e restrições:
- Um conjunto de clientes que possuem sua própria localização(coordenadas)
- Cada cliente possui a sua demanda de quantidade de produtos
- Uma frota limitada de caminhões com uma capacidade máxima de carga que não pode ser excedida
- As rotas devem iniciar e terminar no centro de distribuição da empresa

### Parâmetros utilizados no problema:
- Número de clientes: 15
- Capacidade de carga dos caminhões: 100 lotes de por veículo
- Matriz de distâncias: Representando a distância entre o depósito e os clientes e entre os próprios clientes.
- Demandas: Cada cliente tem uma demanda que vai de 5 a 20 lotes

O desafio é criar rotas que respeitem a capacidade de carga do veículo e minimizem a distância total percorrida.

## Algoritmo Genético
	
Inspirado na evolução natural, tenta "evoluir" uma solução melhor ao longo do tempo (gerações). Ele funciona criando várias soluções (chamadas de "população"), selecionando as melhores, combinando-as e "mutando" algumas delas para tentar encontrar uma solução mais eficiente.

Exploraremos um grande número de soluções através do uso de operadores genéticos como seleção, torneio, elitismo, crossover, mutação e stop(critério de parada).

## Algoritmo Convencional (Método Guloso)

Para a abordagem com o algoritmo convencional, utilizaremos o algoritmo guloso que é uma abordagem direta e intuitiva para a resolução do problema de roteamento. O algoritmo gera decisões com base nas informações locais, buscando sempre o ponto de entrega mais próximo que possa ser atendido pelo caminhão sem exceder sua capacidade de carga.

O algoritmo guloso funciona com base nos seguintes pontos:

Para cada caminhão, o algoritmo seleciona o cliente mais próximo do último cliente atendido (ou do depósito). Os clientes são adicionados ao itinerário de um caminhão até atingir a sua capacidade máxima ou até não haver mais clientes disponíveis. Quando a capacidade do caminhão é atingida ou todos os clientes foram atendidos, o caminhão vai para o centro de distribuição.

## Implementação do algoritmo para a resolução do desafio

### 1. População Inicial:

Neste projeto utilizamos duas aborgagens para a criação da população inicial. Uma aleatória e outra com uma abordagem heurística com o uso do KNN;

#### Método Aleatório
Como comparação, criamos outra população inicial aleatória, onde as rotas são geradas embaralhando a ordem dos clientes. Isso oferece diversidade à população, crucial para evitar que o AG caia em mínimos locais.

#### Método KNN (Nearest Neighbors)
Aqui, utilizamos o algoritmo dos k-vizinhos mais próximos para criar uma população inicial. O KNN tenta construir rotas iniciais razoáveis, baseadas nas distâncias entre clientes próximos. Isso é vantajoso porque evita que o algoritmo comece com rotas completamente aleatórias, o que pode retardar a convergência.
Em nosso projeto realizamos diversos testes variando o `n_neighbors` e a melhor convergência e resultado se estabeleceu para `n_neighbors` igual a 5. 

### 2. Avaliação (Fitness):

A função `calculate_distance` é usada para calcular a distância total percorrida por cada rota. No AG, o fitness de cada indivíduo (solução) é a distância total da rota, com soluções melhores tendo distâncias menores.

- Por quê? A função fitness é essencial para guiar o processo de seleção e reprodução. No VRP, minimizar a distância total é o objetivo principal, então a função fitness diretamente reflete a qualidade de uma solução.

### 3. Seleção por Torneio:
Torneio: Uma técnica de seleção que escolhe um subconjunto de indivíduos da população (o torneio) e seleciona o melhor dentro desse grupo para avançar para a próxima geração.
- Por quê? A seleção por torneio garante que as melhores soluções tenham uma maior chance de reprodução, mas ainda mantém um grau de diversidade, pois soluções menos ótimas ainda podem ser selecionadas.

### 4. Crossover:
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

- Por quê? O algoritmo guloso é simples e rápido, mas não explora o espaço de busca de maneira global, o que o torna uma técnica subótima comparada ao AG, mas útil como comparação.

### Visualização:
A visualização com Pygame permite observar as rotas geradas, ajudando a entender como as soluções evoluem e como o algoritmo otimiza as rotas ao longo do tempo. Além de ser uma ferramenta de validação visual, é útil para explicar a convergência e o comportamento do AG.

### Considerações Finais:

Por fim, com esta simulação, podemos comparar a eficiência dos algoritmos genéticos (População inicial aleatória e com knn) e do guloso aplicado ao VRP (Vehicle Routing Problem).

Inicialmente o guloso performou mais rápido e melhor em comparação ao genético com população inicial aleatória e crossover. Partindo desse ponto de comparação, inserimos:
- Mutação adaptativa: Crucial para ajustar a exploração e exploração ao longo do tempo, evitando a estagnação do algoritmo.
- Elitismo e torneio: Técnicas que garantem um equilíbrio entre exploração (diversidade) e exploração das melhores soluções.
Com essas melhorias o genético começou a performar melhor, encontrando soluções mais otimizada comparada com o guloso.

Na sequência realizamos uma abordagem heurística para a criação da população inicial do genético. Encontrando assim a melhor solução convergindo entre a 1500ª e 2000ª geração, para o contexto em questão:
#### Melhor Solução
- Rota: [4, 9, 7, 12, 10, 11, 14, 3, 1, 6, 5, 13, 8, 2, 15]
- Sub_rotas
  - [0 ,4, 9, 7, 12, 10, 11, 14, 3, 0]
  - [0 ,1, 6, 5, 13, 8, 2, 15, 0]
  - 0 representa o depósito
- Distância: 368

Concluímos que:
- Algoritmo guloso: Simples e rápido, mas geralmente fornece uma solução subótima.
- AG com população inicial aleatória: Explora um espaço de soluções mais diverso, o que pode ajudar a evitar mínimos locais, mas tende a convergir mais lentamente.
- AG com população inicial baseada no KNN: Tendência a convergir mais rapidamente, devido à qualidade inicial da população. E foi quem estabeleceu dentre todas o melhor resultado (menor distância) considerando as demandas de cada cliente e capatidade do veículo.

OBS: Incluímos uma flag em nosso algoritmo `actived_best_value` caso desejem utilizar a melhor solução encontrada durante esses testes como valor inicial de uma nova bateria de testes. Basta setar a flag para `True`.

![Descrição da Imagem](./data/Melhor%20Resultado.jpg)
