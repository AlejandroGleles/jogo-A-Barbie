import random
import time

# Posições dos amigos no mapa
amigos = {
    "Suzy": (4, 12),
    "Polly": (23, 37),
    "Mary": (35, 14),
    "Carly": (5, 34),
    "Ken": (9, 8),
    "Brandon": (36, 36)
}

def a_star(inicio, destino, mapa):
    # Conjunto de posições a serem exploradas
    open_set = {inicio}
    came_from = {}
    
    # Custos iniciais: 0 para o ponto de partida
    g_cost = {inicio: 0}
    f_cost = {inicio: heuristica(inicio, destino)}  # Estimativa inicial para o destino
    
    while open_set:
        # Escolhe o ponto com o menor custo total
        atual = min(open_set, key=lambda x: f_cost.get(x, float('inf')))
        
        # Se chegamos ao destino, reconstruímos o caminho
        if atual == destino:
            return reconstruir_caminho(came_from, atual), g_cost[atual]
        
        open_set.remove(atual)  # Remove o ponto atual da lista de pontos a explorar
        
        # Avalia os vizinhos do ponto atual
        for vizinho in obter_vizinhos(atual, mapa):
            custo = g_cost[atual] + custo_terreno(vizinho, mapa)  # Calcula custo para o vizinho
            
            # Atualiza custos se o caminho for melhor
            if vizinho not in g_cost or custo < g_cost[vizinho]:
                came_from[vizinho] = atual
                g_cost[vizinho] = custo
                f_cost[vizinho] = custo + heuristica(vizinho, destino)
                if vizinho not in open_set:
                    open_set.add(vizinho)  # Adiciona vizinho à lista de pontos a explorar
    
    return [], float('inf')  # Retorna que não foi possível encontrar um caminho

def obter_vizinhos(posicao, mapa):
    vizinhos = []
    x, y = posicao
    
    movimentos = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Direções possíveis
    for dx, dy in movimentos:
        vizinho = (x + dx, y + dy)
        # Verifica se o vizinho está dentro dos limites e é acessível
        if 0 <= vizinho[0] < len(mapa) and 0 <= vizinho[1] < len(mapa[0]) and mapa[vizinho[0]][vizinho[1]] != 0:
            vizinhos.append(vizinho)
    
    return vizinhos

def custo_terreno(posicao, mapa):
    tipo_terreno = mapa[posicao[0]][posicao[1]]
    # Define custos baseados no tipo de terreno
    if tipo_terreno == 1:
        return 1  # Asfalto
    elif tipo_terreno == 3:
        return 3  # Terra
    elif tipo_terreno == 5:
        return 5  # Grama
    elif tipo_terreno == 10:
        return 10  # Paralelepípedo
    return float('inf')  # Terreno intransponível

def heuristica(a, b):
    # Usa a distância Manhattan como estimativa
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruir_caminho(came_from, atual):
    caminho = []
    while atual in came_from:
        caminho.append(atual)
        atual = came_from[atual]
    caminho.reverse()  # Inverte para obter o caminho correto
    return caminho

def sma_star(inicio, destino, mapa, max_depth=10):
    # Lógica semelhante ao A*, mas com uma profundidade máxima
    open_set = {inicio}
    came_from = {}
    
    g_cost = {inicio: 0}
    f_cost = {inicio: heuristica(inicio, destino)}
    
    while open_set:
        atual = min(open_set, key=lambda x: f_cost.get(x, float('inf')))
        
        if atual == destino:
            return reconstruir_caminho(came_from, atual), g_cost[atual]
        
        open_set.remove(atual)

        for vizinho in obter_vizinhos(atual, mapa):
            custo = g_cost[atual] + custo_terreno(vizinho, mapa)
            
            if vizinho not in g_cost or custo < g_cost[vizinho]:
                came_from[vizinho] = atual
                g_cost[vizinho] = custo
                f_cost[vizinho] = custo + heuristica(vizinho, destino)
                if vizinho not in open_set:
                    open_set.add(vizinho)

            # Aqui poderia ser implementada a lógica para limitar a profundidade de busca
            
    return [], float('inf')  # Retorna que não foi possível encontrar um caminho

def missao(mapa, algoritmo):
    casa_barbie = (22, 18)  # Posição inicial da Barbie
    todos_amigos = list(amigos.keys())  # Lista com todos os amigos
    amigos_sorteados = random.sample(todos_amigos, 3)  # Seleciona 3 amigos aleatoriamente
    #amigos_sorteados = ("Suzy","Polly", "Mary")
    amigos_visitados = []  # Lista para os amigos que já foram encontrados
    amigos_restantes = list(amigos.keys())  # Inicialmente, todos os amigos estão disponíveis

    custo_total = 0
    caminho_total = []
    detalhes_caminho = []  # Para detalhes do caminho percorrido

    print(f"Barbie inicia na posição {casa_barbie}.")
    print(f"Amigos sorteados: {amigos_sorteados}\n")

    inicio_tempo = time.time()  # Marca o início do tempo da missão

    # Continua enquanto não encontrou todos os amigos sorteados e ainda há amigos restantes
    while len(amigos_visitados) < 3 and amigos_restantes:
        melhor_amigo = None
        menor_custo = float('inf')  # Começa com custo infinito

        # Avalia cada amigo que ainda precisa ser visitado
        for amigo in amigos_restantes:
            destino = amigos[amigo]
            if algoritmo == "A*":
                caminho, custo = a_star(casa_barbie, destino, mapa)

            if caminho and custo < menor_custo:
                menor_custo = custo
                melhor_amigo = amigo
                melhor_caminho = caminho

        # Verifica se encontrou um caminho viável para algum amigo
        if melhor_amigo:
            caminho_total.extend(melhor_caminho)  # Adiciona o caminho total
            custo_total += menor_custo  # Acumula o custo
            detalhes_caminho.append(f"De {casa_barbie} até {melhor_amigo} na posição {amigos[melhor_amigo]}, custo: {menor_custo}")

            casa_barbie = amigos[melhor_amigo]  # Atualiza a posição da Barbie
            amigos_restantes.remove(melhor_amigo)  # Remove o amigo da lista de amigos restantes

            # Se o amigo visitado estava entre os sorteados
            if melhor_amigo in amigos_sorteados:
                amigos_visitados.append(melhor_amigo)  # Marca o amigo como encontrado
                detalhes_caminho.append(f"{melhor_amigo} foi encontrado! Amigo {len(amigos_visitados)}/3.")

        else:
            print(f"Não foi possível encontrar um caminho para algum amigo.")
            break

    # Se Barbie encontrou todos os amigos sorteados, volta para casa
    if len(amigos_visitados) == 3:
        caminho_de_volta, custo_volta = a_star(casa_barbie, (22, 18), mapa)
        caminho_total.extend(caminho_de_volta)  # Adiciona o caminho de volta
        custo_total += custo_volta  # Acumula o custo da volta

    tempo_execucao = time.time() - inicio_tempo  # Calcula o tempo total da missão
  
    # Retorna os resultados da missão
    print(caminho_total)
    return caminho_total, amigos_visitados, custo_total, tempo_execucao, detalhes_caminho
