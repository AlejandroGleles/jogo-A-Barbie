import tkinter as tk
from matriz import mapa

# Cores correspondentes
cores = {
    0: "orange",     # Caminho (terra)
    5: "green",      # Grama
    3: "brown",      # Terra
    1: "darkgray",   # Asfalto
    10: "lightgray", # Paralelepípedo
}

# Tamanho dos quadrados e espaçamento
tamanho_quadrado = 10
espaco = 0.2  # Tamanho do espaço

# Criação da janela
janela = tk.Tk()
janela.title("Mapa")
janela.config(bg="black")  # Definindo o fundo da janela como preto

# Criação da grade do mapa
for i, linha in enumerate(mapa):
    for j, valor in enumerate(linha):
        cor = cores.get(valor, "black")  # Cor padrão se não encontrado
        
        # Criar quadrado
        quadrado = tk.Frame(janela, width=tamanho_quadrado, height=tamanho_quadrado, bg=cor)
        quadrado.grid(row=i * 2, column=j * 2, padx=0, pady=0)  # A posição do quadrado é multiplicada por 2

        # Criar um quadrado preto para o espaço entre os quadrados (horizontal)
        if j < len(linha) - 1:  # Para não adicionar espaço após o último quadrado da linha
            espaco_vertical = tk.Frame(janela, width=espaco, height=tamanho_quadrado, bg="black")
            espaco_vertical.grid(row=i * 2, column=j * 2 + 1)  # Adiciona o espaço na coluna seguinte

    # Adicionar um espaço preto após cada linha (vertical)
    if i < len(mapa) - 1:
        espaco_horizontal = tk.Frame(janela, width=tamanho_quadrado * len(linha) + espaco * (len(linha) - 1), height=espaco, bg="black")
        espaco_horizontal.grid(row=i * 2 + 1, column=0, columnspan=len(linha) * 2)  # Alinha corretamente as colunas

# Iniciar a interface
janela.mainloop()
