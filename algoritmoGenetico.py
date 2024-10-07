import numpy as np
import random
import pygame
from sklearn.neighbors import NearestNeighbors

# Parâmetros do problema
num_clients = 15
# demands = np.random.randint(5, 21, num_clients)
demands = np.array([11,16,17,12,19,7,18,5,8,6,12,8,6,18,10])
capacity = 100  # Capacidade dos veículos
distance_matrix = np.array([[79, 14, 53, 61, 21, 56, 25, 73, 45, 29, 51, 44, 78, 41, 44, 56],
 [66, 33, 80, 70, 11, 35, 12, 59, 96, 23, 36, 89, 84, 50, 19, 82,],
 [71, 38, 47, 44, 92, 26, 74, 46, 69, 80, 75, 21, 83, 30, 83, 13,],
 [26, 53, 52, 36, 23, 48, 51, 40, 85, 89, 12, 30, 18, 73, 99, 88,],
 [60, 22, 49, 66, 19, 34, 61, 21, 98, 14, 45, 96, 53, 71, 76, 37,],
 [89, 58, 22, 41, 88, 36, 33, 88, 50, 44, 79, 39, 14, 22, 65, 23,],
 [97, 73, 57, 78, 81, 15, 62, 66, 98, 28, 15, 82, 96, 96, 64, 41,],
 [77, 86, 74, 90, 93, 61, 99, 32, 94, 92, 91, 83, 39, 60, 49, 69,],
 [84, 50, 15, 17, 35, 46, 67, 60, 29, 94, 29, 80, 66, 33, 75, 75,],
 [53, 62, 89, 54, 35, 49, 23, 21, 48, 46, 44, 62, 65, 87, 10, 52,],
 [80, 33, 92, 31, 62, 24, 44, 18, 59, 28, 80, 19, 42, 31, 12, 73,],
 [54, 29, 30, 45, 70, 55, 53, 47, 62, 47, 21, 38, 49, 63, 18, 96,],
 [89, 63, 17, 88, 30, 51, 83, 38, 52, 97, 20, 27, 11, 10, 56, 41,],
 [28, 26, 17, 38, 23, 16, 81, 22, 37, 33, 32, 76, 95, 34, 59, 22,],
 [95, 11, 23, 38, 50, 47, 31, 56, 43, 51, 71, 78, 42, 34, 88, 39,],
 [24, 94, 89, 96, 15, 80, 72, 18, 52, 63, 60, 68, 58, 25, 13, 39,]]) 


# Coordenadas fixas dos clientes e depósito
clients_coords = np.array([
    [374.54011884736246, 950.7143064099162],
    [731.993941811405, 598.6584841970366],
    [156.01864044243651, 155.99452033620265],
    [58.083612168199465,	866.1761457749351],
    [601.1150117432088,	708.0725777960456],
    [20.584494295802447,	969.9098521619943],
    [832.4426408004217,	212.33911067827616],
    [181.82496720710063,	183.4045098534338],
    [304.2422429595377,	524.75643163223786],
    [431.94501864211574,	291.22914019804192],
    [611.8528947223795,	139.49386065204184],
    [292.14464853521815,	366.3618432936917],
    [456.06998421703594,	785.1759613930136],
    [199.67378215835975,	514.2344384136116],
    [592.4145688620425,	46.45041271999773],
])
deposit_coord = (500, 400)  # Coordenadas fixas do depósito

# Inicializa o Pygame
pygame.init()
screen_width = 900
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
        total_distance += distance_matrix[0, sub_route[0]]  # Distância do depósito para o primeiro cliente
        for i in range(len(sub_route) - 1):
            total_distance += distance_matrix[sub_route[i], sub_route[i + 1]]
        total_distance += distance_matrix[sub_route[-1], 0]  # Retorno ao depósito
    return total_distance

# Criação da população inicial usando KNN
def create_initial_population_knn(size):
    population = []
    knn = NearestNeighbors(n_neighbors=5)
    knn.fit(clients_coords)

    for _ in range(size):
        route = []
        remaining_clients = list(range(1, num_clients + 1))  # Clientes de 1 a num_clients
        current_client = 0  # Começa no depósito

        while remaining_clients:
            distances, indices = knn.kneighbors([clients_coords[current_client]], n_neighbors=5)
            next_client = None
            
            for idx in indices[0]:
                client_id = remaining_clients[idx - 1]  
                demand = demands[client_id - 1]  

                if demand <= capacity:  
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
        route = list(range(1, num_clients + 1))  # Clientes de 1 a num_clients
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
        demand = demands[client - 1]  
        if current_capacity + demand <= capacity:
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
def genetic_algorithm(population_size, generations, population_method='knn', initial_value = None):
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
        
        visualize(best_solution)

    return best_solution, best_distance

# Função de visualização
def visualize(solution):
    screen.fill((255, 255, 255))
    
    pygame.draw.circle(screen, (0, 255, 0), deposit_coord, 10)  
    
    for i, coord in enumerate(clients_coords):
        pygame.draw.circle(screen, (0, 0, 255), coord, 5)  
    
    routes = to_routes(solution)
    for sub_route in routes:
        route_with_deposit = [0] + sub_route + [0]  
        for i in range(len(route_with_deposit) - 1):
            pygame.draw.line(screen, (255, 0, 0), 
                             clients_coords[route_with_deposit[i] - 1] if route_with_deposit[i] != 0 else deposit_coord,
                             clients_coords[route_with_deposit[i + 1] - 1] if route_with_deposit[i + 1] != 0 else deposit_coord,
                             2)  

    pygame.display.flip()
    clock.tick(60)  

# Implementação do Algoritmo Guloso
def greedy_algorithm():
    routes = []
    remaining_clients = list(range(1, num_clients + 1))  

    while remaining_clients:
        current_route = []
        current_capacity = 0
        current_client = 0  

        while True:
            next_client = None
            min_distance = float('inf')

            for client in remaining_clients:
                demand = demands[client - 1]
                if current_capacity + demand <= capacity:
                    distance_to_client = distance_matrix[current_client, client]
                    if distance_to_client < min_distance:
                        min_distance = distance_to_client
                        next_client = client
            
            if next_client is not None:
                current_route.append(next_client)
                current_capacity += demands[next_client - 1]
                remaining_clients.remove(next_client)
                current_client = next_client  
            else:
                break
        
        routes.append(current_route)

    return routes

# Execução dos Algoritmos e Comparação
if __name__ == "__main__":
    num_iterations = 5  # Número de iterações para melhorar a solução
    generations=5000
    best_value = [4, 9, 7, 12, 10, 11, 14, 3, 1, 6, 5, 13, 8, 2, 15]
    # Executa o Algoritmo Genético com o método KNN
    best_solution_genetic_knn = best_value
    for i in range(num_iterations):
        best_solution_genetic_knn, best_distance_genetic_knn = genetic_algorithm(population_size=50, generations=generations, population_method='knn', initial_value = best_solution_genetic_knn)

    # Executa o Algoritmo Genético com o método aleatório
    best_solution_genetic = best_value
    for i in range(num_iterations):
        best_solution_genetic_random, best_distance_genetic_random = genetic_algorithm(population_size=50, generations=generations, population_method='random', initial_value = best_solution_genetic)

    # Executa o Algoritmo Guloso
    greedy_solution = greedy_algorithm()
    greedy_distance_greedy = calculate_distance(greedy_solution)
    print('ultimo_knn: 392', 'ultimo_random: 434', 'guloso: 498')
    
    print("Melhor distância encontrada (Genético KNN):", best_distance_genetic_knn)
    print("Melhor solução encontrada (Genético KNN):", best_solution_genetic_knn)
    print("Melhor distância encontrada (Genético Aleatório):", best_distance_genetic_random)
    print("Melhor solução encontrada (Genético Aleatório):", best_solution_genetic_random)
    print("Distância total (Gulosa):", greedy_distance_greedy)
    print("Melhor solução encontrada (Gulosa):", greedy_solution)
   
