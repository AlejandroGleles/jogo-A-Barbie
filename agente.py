import random
import heapq

# Posições dos amigos no mapa
amigos = {
    "Suzy": (13, 5),
    "Polly": (38, 23),
    "Mary": (15, 36),
    "Carly": (35, 6),
    "Ken": (9, 10),
    "Brandon": (37, 37)
}

# Escolha aleatória de três amigos que aceitarão o convite
amigos_que_aceitam = random.sample(list(amigos.keys()), 3)

# Algoritmo A* para encontrar o caminho
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(inicio, destino, mapa):
    open_set = []
    heapq.heappush(open_set, (0, inicio))

    g_cost = {inicio: 0}
    f_cost = {inicio: heuristica(inicio, destino)}

    came_from = {}

    while open_set:
        _, atual = heapq.heappop(open_set)

        if atual == destino:
            return reconstruir_caminho(came_from, atual), g_cost[destino]  # Retorna o caminho e o custo final

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vizinho = (atual[0] + dx, atual[1] + dy)

            # Verifica se o vizinho está dentro do mapa e não é uma construção (valor 0)
            if (0 <= vizinho[0] < len(mapa) and
                    0 <= vizinho[1] < len(mapa[0]) and
                    mapa[vizinho[0]][vizinho[1]] != 0):  # Evitar construções (valor 0)

                custo = g_cost[atual] + mapa[vizinho[0]][vizinho[1]]  # Custo baseado no tipo de terreno

                if vizinho not in g_cost or custo < g_cost[vizinho]:
                    came_from[vizinho] = atual
                    g_cost[vizinho] = custo
                    f_cost[vizinho] = custo + heuristica(vizinho, destino)

                    if vizinho not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_cost[vizinho], vizinho))

    return None, float('inf')  # Caso não encontre caminho, retorna custo infinito

def reconstruir_caminho(came_from, atual):
    caminho = []
    while atual in came_from:
        caminho.append(atual)
        atual = came_from[atual]
    caminho.reverse()
    return caminho

def missao(mapa):
    casa_barbie = (19, 23)
    caminho_total = []
    custo_total = 0

    for amigo in amigos_que_aceitam:
        destino = amigos[amigo]
        caminho, custo = a_star(casa_barbie, destino, mapa)

        if caminho:
            caminho_total.extend(caminho)
            custo_total += custo
            casa_barbie = destino  # Atualiza a casa Barbie para o destino atual

    # Voltar para a Casa da Barbie
    caminho_para_casa, custo_para_casa = a_star(casa_barbie, (19, 23), mapa)

    if caminho_para_casa:
        caminho_total.extend(caminho_para_casa)
        custo_total += custo_para_casa

    return caminho_total, custo_total, amigos_que_aceitam  # Retorna o caminho total, o custo e os amigos convencidos
