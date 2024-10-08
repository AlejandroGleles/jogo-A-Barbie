import tkinter as tk
from matriz import mapa

# Posições dos amigos no mapa
amigos = {
    "Suzy": (13, 5),
    "Polly": (38, 23),
    "Mary": (15, 36),
    "Carly": (35, 6),
    "Ken": (9, 10),
    "Brandon": (37, 37)
}

# Função para criar a interface inicial com o botão "Iniciar Jogo"
def criar_interface_inicial(janela, iniciar_jogo_callback):
    janela.title("Jogo da Barbie")
    
    # Título
    titulo = tk.Label(janela, text="Jogo da Barbie", font=("Arial", 24), fg="pink", bg="black")
    titulo.pack(pady=20)

    # Botão para iniciar o jogo
    botao_iniciar = tk.Button(janela, text="Iniciar Jogo", command=iniciar_jogo_callback, font=("Arial", 14), fg="white", bg="pink")
    botao_iniciar.pack(pady=20)

# Função para mostrar o caminho célula por célula
def mostrar_caminho(janela, mapa, caminho_barbie, amigos_convidados, custo_total, delay=200):
    # Cores correspondentes
    cores = {
        0: "orange",     # Caminho (terra)
        5: "green",      # Grama
        3: "brown",      # Terra
        1: "darkgray",   # Asfalto
        10: "lightgray", # Paralelepípedo
        "barbie": "pink",  # Cor da Barbie
        "amigo": "blue",   # Cor dos amigos
        "caminho": "yellow"  # Cor do caminho percorrido
    }

    tamanho_quadrado = 10
    espaco = 0.2  # Tamanho do espaço

    # Função para desenhar a célula específica
    def desenhar_celula(i, j, cor):
        quadrado = tk.Frame(janela, width=tamanho_quadrado, height=tamanho_quadrado, bg=cor)
        quadrado.grid(row=i * 2, column=j * 2, padx=0, pady=0)

    # Função para desenhar o mapa com as posições iniciais
    def desenhar_mapa():
        for i, linha in enumerate(mapa):
            for j, valor in enumerate(linha):
                cor = cores.get(valor, "black")  # Cor padrão se não encontrado

                # Desenhar amigos
                for amigo in amigos_convidados:
                    if (i, j) == amigos[amigo]:
                        cor = cores["amigo"]

                # Desenhar a posição inicial da Barbie
                if (i, j) == (19, 23):  # Posição inicial da Barbie
                    cor = cores["barbie"]

                desenhar_celula(i, j, cor)

    # Função recursiva para atualizar o caminho gradualmente
    def atualizar_caminho(indice=0):
        if indice < len(caminho_barbie):
            i, j = caminho_barbie[indice]
            desenhar_celula(i, j, cores["caminho"])
            janela.after(delay, atualizar_caminho, indice + 1)
        else:
            # Exibe o custo total quando o caminho termina
            custo_label = tk.Label(janela, text=f"Custo Total: {custo_total}", font=("Arial", 14), fg="white", bg="black")
            custo_label.pack(pady=20)

    # Desenhar o mapa inicial
    desenhar_mapa()

    # Começa a exibir o caminho célula por célula
    atualizar_caminho()

# Função para criar a interface completa
def criar_interface(mapa, caminho_barbie, amigos_convidados, custo_total):
    janela = tk.Tk()
    janela.config(bg="black")

    def iniciar_jogo():
        # Limpa a tela inicial e começa o jogo
        for widget in janela.winfo_children():
            widget.destroy()
        mostrar_caminho(janela, mapa, caminho_barbie, amigos_convidados, custo_total)

    # Chama a interface inicial com o botão "Iniciar Jogo"
    criar_interface_inicial(janela, iniciar_jogo)

    janela.mainloop()
