from matriz import mapa
from interface import criar_interface
from agente import missao  # Aqui deve ser o nome correto da função

def main():
    # Iniciar a missão
    caminho, custo_total, amigos_convidados = missao(mapa)  # Recebe o caminho, custo e amigos

    # Criar a interface gráfica com o caminho, amigos e custo
    criar_interface(mapa, caminho, amigos_convidados, custo_total)

if __name__ == "__main__":
    main()
