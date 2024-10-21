import tkinter as tk
from matriz import mapa
from agente import amigos, missao  # Certifique-se de que a importação está correta

def criar_interface_inicial(janela, iniciar_jogo_callback):
    janela.title("Jogo da Barbie")
    
    titulo = tk.Label(janela, text="Jogo da Barbie", font=("Arial", 24), fg="pink", bg="black")
    titulo.grid(row=0, column=0, pady=20)

    algoritmo_var = tk.StringVar(value="A*")  # Valor padrão

    botao_iniciar = tk.Button(janela, text="Iniciar Jogo", command=lambda: iniciar_jogo_callback(algoritmo_var.get()), font=("Arial", 14), fg="white", bg="pink")
    botao_iniciar.grid(row=4, column=0, pady=20)

def mostrar_caminho(janela, mapa, caminho_barbie, amigos_convidados, custo_total, tempo_execucao, delay=100):
    # Cores correspondentes
    cores = {
        0: "orange",     # Edifícios
        5: "green",      # Grama
        3: "brown",      # Terra
        1: "darkgray",   # Asfalto
        10: "lightgray", # Paralelepípedo
        "barbie": "red",  # Cor da Barbie
        "amigo": "blue",   # Cor dos amigos
        "caminho": "yellow"  # Cor do caminho percorrido
    }
    
    # Label para mostrar o tempo de execução
    tempo_label = tk.Label(janela, text="", font=("Arial", 14), fg="white", bg="black")
    tempo_label.grid(row=len(mapa) + 1, column=0, pady=10)

    custo_label = tk.Label(janela, text=f"Custo Total: {custo_total}", font=("Arial", 14), fg="white", bg="black")
    custo_label.grid(row=len(mapa), column=0, pady=10)

    tamanho_quadrado = 10

    def desenhar_celula(i, j, cor):
        quadrado = tk.Frame(janela, width=tamanho_quadrado, height=tamanho_quadrado, bg=cor)
        quadrado.grid(row=i, column=j, padx=0, pady=0)

    def desenhar_mapa():
        for i, linha in enumerate(mapa):
            for j, valor in enumerate(linha):
                cor = cores.get(valor, "black")

                for amigo in amigos:
                    if (i, j) == amigos[amigo]:
                        cor = cores["amigo"]

                # Ajuste aqui para usar (22, 18) como a posição inicial, correspondente a (23, 19)
                if (i, j) == (22, 18):
                    cor = cores["barbie"]

                desenhar_celula(i, j, cor)

    def atualizar_caminho(indice=0):
        if indice < len(caminho_barbie):
            i, j = caminho_barbie[indice]
            desenhar_celula(i, j, cores["barbie"])  # Atualiza a posição da Barbie
            if indice > 0:  # A célula atrás da Barbie
                i_anterior, j_anterior = caminho_barbie[indice - 1]
                desenhar_celula(i_anterior, j_anterior, cores["caminho"])  # Célula anterior em amarelo
            tempo_label.config(text=f"Tempo de Execução: {tempo_execucao:.2f} segundos")
            janela.after(delay, atualizar_caminho, indice + 1)
        else:
            tempo_label.config(text=f"Tempo de Execução: {tempo_execucao:.2f} segundos")  # Atualiza ao final

    desenhar_mapa()
    atualizar_caminho()

def criar_interface(mapa):
    janela = tk.Tk()
    janela.config(bg="black")

    def iniciar_jogo(algoritmo):
        for widget in janela.winfo_children():
            widget.destroy()
        # Aqui você chama a função `missao` e obtém os resultados
        caminho_barbie, amigos_convidados, custo_total, tempo_execucao = missao(mapa, algoritmo)
        mostrar_caminho(janela, mapa, caminho_barbie, amigos_convidados, custo_total, tempo_execucao)

    criar_interface_inicial(janela, iniciar_jogo)
    janela.mainloop()

# Chame criar_interface(mapa) para iniciar o jogo.
