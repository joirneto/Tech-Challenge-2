import numpy as np
import random
import pygame
from sklearn.neighbors import NearestNeighbors

# Parâmetros do problema
num_clientes = 15  # Número de clientes
capacidade_veiculo = 100  # Capacidade dos veículos
demandas_clientes = np.loadtxt('./data/demandas_clientes.csv', delimiter=',') # Demandas dos clientes
matriz_distancia = np.loadtxt('./data/matriz_distancia.csv', delimiter=',') # Matriz de distância

# Coordenadas fixas dos clientes e depósito
coordenadas_clientes = np.loadtxt('./data/coordenadas_clientes.csv', delimiter=',') 
deposit_coord = (500, 400) 

# Inicializa o Pygame
pygame.init()
screen_width = 1000
screen_height = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Algoritmos Genéticos e Guloso - Roteamento de Veículos')
clock = pygame.time.Clock()

# Função para calcular a distância total de uma rota
def calculate_distance(route):
    total_distance = 0
    for sub_route in route:
        if not sub_route:
            continue
        total_distance += matriz_distancia[0, sub_route[0]]  # Distância do depósito para o primeiro cliente
        for i in range(len(sub_route) - 1):
            total_distance += matriz_distancia[sub_route[i], sub_route[i + 1]]
        total_distance += matriz_distancia[sub_route[-1], 0]  # Retorno ao depósito
    return total_distance

# Criação da população inicial usando KNN
def create_initial_population_knn(size):
    population = []
    knn = NearestNeighbors(n_neighbors=5)
    knn.fit(coordenadas_clientes)

    for _ in range(size):
        route = []
        remaining_clients = list(range(1, num_clientes + 1))  # Clientes de 1 a num_clientes
        current_client = 0  # Começa no depósito

        while remaining_clients:
            distances, indices = knn.kneighbors([coordenadas_clientes[current_client]], n_neighbors=5)
            next_client = None
            
            for idx in indices[0]:
                client_id = remaining_clients[idx - 1]  
                demand = demandas_clientes[client_id - 1]  

                if demand <= capacidade_veiculo:  
                    next_client = client_id
                    break
            
            if next_client is not None:
                route.append(next_client)
                remaining_clients.remove(next_client)
                current_client = next_client - 1  
            else:
                break
        
        if route:  
            population.append(route)

    return population

# Criação da população inicial aleatória
def create_initial_population(size):
    population = []
    for _ in range(size):
        route = list(range(1, num_clientes + 1))  # Clientes de 1 a num_clientes
        random.shuffle(route)
        population.append(route)
    return population

# Função de seleção por torneio
def tournament_selection(population, tournament_size=5):
    selected = []
    for _ in range(len(population) // 2):
        competitors = random.sample(population, tournament_size)
        winner = min(competitors, key=lambda r: calculate_distance(to_routes(r)))
        selected.append(winner)
    return selected

# Função de crossover baseado em Ordered Crossover (OX)
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]
    pointer = end
    for gene in parent2:
        if gene not in child:
            if pointer == size:
                pointer = 0
            child[pointer] = gene
            pointer += 1
    return child

# Função de mutação adaptativa (taxa de mutação diminui com o tempo)
def mutate(route, generation, max_generations):
    mutation_rate = max(0.05, 0.2 * (1 - generation / max_generations))  # Decresce com o tempo
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(route)), 2)
        route[idx1], route[idx2] = route[idx2], route[idx1]

# Função que converte uma rota em múltiplas rotas viáveis com base na capacidade do veículo
def to_routes(route):
    routes = []
    current_route = []
    current_capacity = 0
    
    for client in route:
        demand = demandas_clientes[client - 1]  
        if current_capacity + demand <= capacidade_veiculo:
            current_route.append(client)
            current_capacity += demand
        else:
            if current_route:  
                routes.append(current_route)
            current_route = [client]
            current_capacity = demand
            
    if current_route:  
        routes.append(current_route)
    
    return routes

# Algoritmo Genético com as melhorias
def genetic_algorithm(population_size,
                      generations,
                      population_method='knn',
                      initial_value=None,
                      no_improvement_limit=1000):

    if population_method == 'knn':
        population = create_initial_population_knn(population_size)
        if initial_value is not None:
            population[0] = initial_value
    elif population_method == 'random':
        population = create_initial_population(population_size)
        if initial_value is not None:
            population[0] = initial_value
    
    best_solution = min(population, key=lambda r: calculate_distance(to_routes(r)))
    best_distance = calculate_distance(to_routes(best_solution))
    
    # Contador de gerações sem melhoria
    generations_without_improvement = 0

    for generation in range(generations):
        print(f"Geração {generation}: Melhor distância (Genético, {population_method}) = {best_distance}")
        selected = tournament_selection(population)
        
        # Elitismo: preserva o melhor indivíduo
        next_generation = [best_solution] + selected.copy()
        
        # Gera a próxima geração
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = crossover(parent1, parent2)
            mutate(child, generation, generations)
            next_generation.append(child)

        population = next_generation
        current_best = min(population, key=lambda r: calculate_distance(to_routes(r)))
        current_distance = calculate_distance(to_routes(current_best))
        
        if current_distance < best_distance:
            best_solution = current_best
            best_distance = current_distance
            generations_without_improvement = 0  # Reiniciar o contador quando há melhoria
        else:
            generations_without_improvement += 1  # Incrementar o contador se não houver melhoria
        
        # Verificar se excedeu o limite de gerações sem melhoria
        if generations_without_improvement >= no_improvement_limit:
            print(f"Interrompendo a execução após {generation} gerações devido à falta de melhoria.")
            break
        
        visualize(best_solution)

    return best_solution, best_distance


# Função de visualização
# Lista de nomes dos clientes e do depósito
nomes_clientes = ["Depósito"] + [f"Cliente {i}" for i in range(1, num_clientes + 1)]

# Função de visualização
def visualize(solution):
    screen.fill((255, 255, 255))  # Limpa a tela (branco)
    
    # Fonte para desenhar os nomes
    font = pygame.font.Font(None, 24)  # Usa a fonte padrão, tamanho 24
    
    # Desenha o depósito
    pygame.draw.circle(screen, (0, 255, 0), deposit_coord, 10)  # Círculo para o depósito
    text_surface = font.render(nomes_clientes[0], True, (0, 0, 0))  # Renderiza o nome "Depósito"
    screen.blit(text_surface, (deposit_coord[0] + 10, deposit_coord[1]))  # Desenha o nome ao lado do depósito
    
    # Desenha os clientes
    for i, coord in enumerate(coordenadas_clientes):
        pygame.draw.circle(screen, (0, 0, 255), coord, 5)  # Círculo para os clientes
        text_surface = font.render(nomes_clientes[i + 1], True, (0, 0, 0))  # Renderiza o nome do cliente
        screen.blit(text_surface, (coord[0] + 10, coord[1]))  # Desenha o nome ao lado do cliente
    
    # Desenha as rotas
    routes = to_routes(solution)
    for sub_route in routes:
        route_with_deposit = [0] + sub_route + [0]  # Rota incluindo o depósito
        for i in range(len(route_with_deposit) - 1):
            pygame.draw.line(screen, (255, 0, 0), 
                             coordenadas_clientes[route_with_deposit[i] - 1] if route_with_deposit[i] != 0 else deposit_coord,
                             coordenadas_clientes[route_with_deposit[i + 1] - 1] if route_with_deposit[i + 1] != 0 else deposit_coord,
                             2)  # Desenha a linha conectando os clientes

    pygame.display.flip()
    clock.tick(60)  # Atualiza a tela com taxa de quadros de 60 FPS
 

# Implementação do Algoritmo Guloso
def greedy_algorithm():
    routes = []
    remaining_clients = list(range(1, num_clientes + 1))  

    while remaining_clients:
        current_route = []
        current_capacity = 0
        current_client = 0  

        while True:
            next_client = None
            min_distance = float('inf')

            for client in remaining_clients:
                demand = demandas_clientes[client - 1]
                if current_capacity + demand <= capacidade_veiculo:
                    distance_to_client = matriz_distancia[current_client, client]
                    if distance_to_client < min_distance:
                        min_distance = distance_to_client
                        next_client = client
            
            if next_client is not None:
                current_route.append(next_client)
                current_capacity += demandas_clientes[next_client - 1]
                remaining_clients.remove(next_client)
                current_client = next_client  
            else:
                break
        
        routes.append(current_route)

    return routes

# Execução dos Algoritmos e Comparação
if __name__ == "__main__":
    num_iterations = 10  # Número de iterações para melhorar a solução
    generations=3000

    best_value = [4, 9, 7, 12, 10, 11, 14, 3, 1, 6, 5, 13, 8, 2, 15]
    actived_best_value = True

    if not actived_best_value:
        best_value = None

    # Executa o Algoritmo Genético com o método KNN
    best_solution_genetic_knn = best_value
    for i in range(num_iterations):
        best_solution_genetic_knn, best_distance_genetic_knn = genetic_algorithm(
            population_size=50,
            generations=generations,
            population_method='knn',
            initial_value = best_solution_genetic_knn,
            no_improvement_limit=1000)

    # Executa o Algoritmo Genético com o método aleatório
    best_solution_genetic = best_value
    for i in range(num_iterations):
        best_solution_genetic_random, best_distance_genetic_random = genetic_algorithm(
            population_size=50,
            generations=generations,
            population_method='random',
            initial_value = best_solution_genetic,
            no_improvement_limit=1000)

    # Executa o Algoritmo Guloso
    greedy_solution = greedy_algorithm()
    greedy_distance_greedy = calculate_distance(greedy_solution)
       
    print("Melhor distância encontrada (Genético KNN):", best_distance_genetic_knn)
    print("Melhor solução encontrada (Genético KNN):", best_solution_genetic_knn)
    print("Melhor distância encontrada (Genético Aleatório):", best_distance_genetic_random)
    print("Melhor solução encontrada (Genético Aleatório):", best_solution_genetic_random)
    print("Distância total (Gulosa):", greedy_distance_greedy)
    print("Melhor solução encontrada (Gulosa):", greedy_solution)
   
