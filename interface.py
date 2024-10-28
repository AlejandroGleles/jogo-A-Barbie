import tkinter as tk
from agente import amigos, missao 

def centralizar_janela(janela, largura, altura):
    # Configura a janela com as dimensões e a centraliza na tela
    janela.geometry(f"{largura}x{altura}")
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def criar_interface_inicial(janela, iniciar_jogo_callback):
    # Define o título e a cor de fundo da janela
    janela.title("Jogo da Barbie")
    janela.config(bg="black")
    centralizar_janela(janela, largura=400, altura=300)

    # Cria um frame para organizar os widgets
    frame_conteudo = tk.Frame(janela, bg="black")
    frame_conteudo.pack(expand=True)

    # Título do jogo
    titulo = tk.Label(frame_conteudo, text="Jogo da Barbie", font=("Arial", 24), fg="pink", bg="black")
    titulo.pack(pady=20)

    algoritmo_var = tk.StringVar(value="A*")  # Define A* como algoritmo padrão

    # Botão para iniciar o jogo
    botao_iniciar = tk.Button(frame_conteudo, text="Iniciar Jogo", command=lambda: iniciar_jogo_callback(algoritmo_var.get()), font=("Arial", 14), fg="white", bg="pink")
    botao_iniciar.pack(pady=20)

def mostrar_caminho(janela, mapa, caminho_barbie, amigos_visitados, custo_total, tempo_execucao, detalhes_caminho, delay=100):
    # Define cores para diferentes elementos do mapa
    cores = {
        0: "#f79646",     # Edifícios
        5: "#92d050",      # Grama
        3: "brown",      # Terra
        1: "darkgray",   # Asfalto
        10: "lightgray", # Paralelepípedo
        "barbie": "red",  # Cor da Barbie
        "amigo": "blue",   # Cor dos amigos
        "caminho": "yellow"  # Cor do caminho percorrido
    }
    
    # Configura a janela para ocupar 80% da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    largura_janela = int(largura_tela * 0.8)
    altura_janela = int(altura_tela * 0.8)
    centralizar_janela(janela, largura_janela, altura_janela)

    # Cria um frame para exibir as estatísticas do jogo
    frame_estatisticas = tk.Frame(janela, bg="black")
    frame_estatisticas.grid(row=0, column=len(mapa[0]), rowspan=len(mapa), padx=20)

    # Labels para mostrar a posição inicial e amigos visitados
    posicao_label = tk.Label(frame_estatisticas, text="Barbie inicia na posição (22, 18).", font=("Arial", 14), fg="white", bg="black")
    posicao_label.pack(pady=5)

    amigos_label = tk.Label(frame_estatisticas, text=f"Amigos sorteados: {', '.join(amigos_visitados)}", font=("Arial", 14), fg="white", bg="black")
    amigos_label.pack(pady=5)

    # Exibe detalhes do caminho
    for detalhe in detalhes_caminho:
        detalhe_label = tk.Label(frame_estatisticas, text=detalhe, font=("Arial", 12), fg="white", bg="black")
        detalhe_label.pack(pady=2)

    # Exibe custo total e tempo de execução
    custo_label = tk.Label(frame_estatisticas, text=f"Custo Total: {custo_total}", font=("Arial", 14), fg="white", bg="black")
    custo_label.pack(pady=5)

    tempo_label = tk.Label(frame_estatisticas, text=f"Tempo de Execução: {tempo_execucao:.2f} segundos", font=("Arial", 14), fg="white", bg="black")
    tempo_label.pack(pady=5)

    tamanho_quadrado = 14  # Tamanho de cada célula do mapa

    # Função para desenhar uma célula no mapa
    def desenhar_celula(i, j, cor):
        quadrado = tk.Frame(janela, width=tamanho_quadrado, height=tamanho_quadrado, bg=cor)
        quadrado.grid(row=i, column=j, padx=0, pady=0)

    # Função para desenhar o mapa com base nos dados fornecidos
    def desenhar_mapa():
        for i, linha in enumerate(mapa):
            for j, valor in enumerate(linha):
                cor = cores.get(valor, "black")  # Define a cor da célula
                for amigo in amigos:
                    if (i, j) == amigos[amigo]:
                        cor = cores["amigo"]  # Se a posição é de um amigo, usa a cor correspondente
                if (i, j) == (22, 18):
                    cor = cores["barbie"]  # Marca a posição da Barbie
                desenhar_celula(i, j, cor)  # Desenha a célula no mapa

    # Função para atualizar a animação do caminho
    def atualizar_caminho(indice=0):
        if indice < len(caminho_barbie):
            i, j = caminho_barbie[indice]
            desenhar_celula(i, j, cores["barbie"])  # Desenha a posição atual da Barbie
            if indice > 0:
                i_anterior, j_anterior = caminho_barbie[indice - 1]
                desenhar_celula(i_anterior, j_anterior, cores["caminho"])  # Desenha o caminho percorrido
            tempo_label.config(text=f"Tempo de Execução: {tempo_execucao:.2f} segundos")
            janela.after(delay, atualizar_caminho, indice + 1)  # Chama a função novamente após um atraso
        else:
            tempo_label.config(text=f"Tempo de Execução: {tempo_execucao:.2f} segundos")  # Atualiza o tempo final

    desenhar_mapa()  # Desenha o mapa inicialmente
    atualizar_caminho()  # Inicia a animação do caminho

def criar_interface(mapa):
    janela = tk.Tk()  # Cria a janela principal

    # Função chamada quando o jogo é iniciado
    def iniciar_jogo(algoritmo):
        # Limpa a tela da janela para iniciar um novo jogo
        for widget in janela.winfo_children():
            widget.destroy()
        # Chama a função `missao` e obtém os resultados do jogo
        caminho_barbie, amigos_convidados, custo_total, tempo_execucao, detalhes_caminho = missao(mapa, algoritmo)
        # Mostra o caminho e as estatísticas na tela
        mostrar_caminho(janela, mapa, caminho_barbie, amigos_convidados, custo_total, tempo_execucao, detalhes_caminho)

    criar_interface_inicial(janela, iniciar_jogo)  # Cria a interface inicial
    janela.mainloop()  # Inicia o loop principal da interface gráfica

# Para iniciar o jogo, chame criar_interface(mapa).
