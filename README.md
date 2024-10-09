# POS FIAP ALURA - IA PARA DEVS
## Tech Challenge Fase 2
### Integrantes Grupo 26

- André Philipe Oliveira de Andrade(RM357002) - andrepoandrade@gmail.com
- Joir Neto (RM356391) - joirneto@gmail.com
- Marcos Jen San Hsie(RM357422) - marcosjsh@gmail.com
- Michael dos Santos Silva(RM357009) - michael.shel96@gmail.com
- Sonival dos Santos(RM356905) - sonival.santos@gmail.com

Youtube: 

## Descrição do problema: Vehicle Routing Problem

Vehicle Routing Problem ou VRP é um problema de otimização de rotas comum no setor de logística e distribuição que pode ser resolvido com o uso de algoritmos genéticos. Este problema se baseia na otimização de rotas que uma frota de veículos pode seguir para atender as demandas de entrega de uma lista de clientes, considerando algumas restrições como a capacidade dos veículos e em alguns casos específicos, janelas de tempo específicas para entrega.
Neste projeto, faremos o uso de um algoritmo convencional e um algoritmo genético para elaborar uma solução para o caso fictício da Bem-Te-Vi Logística e da CasaBella Pisos e Revestimentos. O objetivo é minimizar o custo logístico através da diminuição da distância percorrida pelos veículos, mantendo a segurança ao não ultrapassar os limites de carga, garantindo com que todos os clientes sejam atendidos.

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

## Algoritmo Genético
	
Para a abordagem com o algoritmo genético, utilizaremos técnicas inspiradas na evolução natural para encontrar soluções otimizadas. Exploraremos um grande número de soluções através do uso de operadores genéticos como seleção, crossover e mutação.

O algoritmo genético criado para este projeto, funciona da seguinte forma:

## Algoritmo Convencional (Método Guloso)

Para a abordagem com o algoritmo convencional, utilizaremos o algoritmo guloso que é uma abordagem direta e intuitiva para a resolução do problema de roteamento. O algoritmo gera decisões com base nas informações locais, buscando sempre o ponto de entrega mais próximo que possa ser atendido pelo caminhão sem exceder sua capacidade de carga.
O algoritmo guloso funciona com base nos seguintes pontos:

Para cada caminhão, o algoritmo seleciona o cliente mais próximo do último cliente atendido(ou do depósito)
Os clientes são adicionados ao itinerário de um caminhão até atingir a sua capacidade máxima ou até não haver mais clientes disponíveis
Quando a capacidade do caminhão é atingida ou todos os clientes foram atendidos, o caminhão vai para o centro de distribuição


Observações
Algoritmo Convencional (Método Guloso):
Gera uma solução rápida baseado apenas em informações locais
Pode vir a ser eficiente em cenários mais simples
Devido ao fato de não explorar mais a fundo outras soluções, pode gerar resultados subótimos

Algoritmo Genético:
Explora um número de soluções muito maior
A qualidade das soluções melhora ao longo das gerações
Foi capaz de gerar uma solução com custo total de distância significativamente menor graças a exploração de combinações de rotas que o algoritmo guloso não iria simular


## Conclusão

Com esta simulação, podemos comparar a eficiência dos algoritmos guloso e genético aplicado ao VRP (Vehicle Routing Problem). Enquanto o algoritmo guloso, gerou uma solução rápida, o algoritmo genético através de sua capacidade de explorar o espaço de soluções de modo mais abrangente, nos trouxe uma solução com custo total menor.

Principais Conclusões:
O algoritmo guloso é útil em um contexto de necessidade de respostas rápidas
O algoritmo genético apesar de levar mais tempo para finalização, foi mais eficaz na minimização do custo total de distância 
Combinar técnicas evolutivas e otimização local, gerando assim um algoritmo memético pode ser uma abordagem muito eficiente no sentido de melhorar a qualidade das soluções



