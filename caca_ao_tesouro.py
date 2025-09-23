import pygame
import random
import cores # Importa o módulo de cores, como no exemplo da aula

# --- Funções Auxiliares ---
# Para melhor organização e atender ao requisito de "Funções",
# a lógica de criação do tabuleiro foi separada em uma função.

def inicializar_tabuleiro(linhas, colunas, num_tesouros, num_buracos):
    """
    Cria o tabuleiro do jogo, distribui os tesouros e buracos,
    e calcula os números das casas vizinhas.
    """
    # 1. Começa com um tabuleiro vazio (usando 0 como marcador)
    tabuleiro = [[0 for _ in range(colunas)] for _ in range(linhas)]

    # 2. Distribui os tesouros ('T') aleatoriamente
    tesouros_plantados = 0
    while tesouros_plantados < num_tesouros:
        l = random.randint(0, linhas - 1)
        c = random.randint(0, colunas - 1)
        if tabuleiro[l][c] == 0:
            tabuleiro[l][c] = 'T'
            tesouros_plantados += 1

    # 3. Distribui os buracos ('B') aleatoriamente
    buracos_plantados = 0
    while buracos_plantados < num_buracos:
        l = random.randint(0, linhas - 1)
        c = random.randint(0, colunas - 1)
        if tabuleiro[l][c] == 0:
            tabuleiro[l][c] = 'B'
            buracos_plantados += 1

    # 4. Calcula os números para as casas restantes
    for l in range(linhas):
        for c in range(colunas):
            if tabuleiro[l][c] == 0:
                # Conta quantos tesouros existem nos vizinhos (horizontal e vertical)
                vizinhos = 0
                # Vizinho de cima
                if l > 0 and tabuleiro[l-1][c] == 'T':
                    vizinhos += 1
                # Vizinho de baixo
                if l < linhas - 1 and tabuleiro[l+1][c] == 'T':
                    vizinhos += 1
                # Vizinho da esquerda
                if c > 0 and tabuleiro[l][c-1] == 'T':
                    vizinhos += 1
                # Vizinho da direita
                if c < colunas - 1 and tabuleiro[l][c+1] == 'T':
                    vizinhos += 1
                
                tabuleiro[l][c] = str(vizinhos) # Converte para string para manter o tipo consistente
    
    return tabuleiro

def desenhar_tabuleiro(tela, tabuleiro_visivel, tabuleiro_solucao, lado_celula, fonte, img_tesouro, img_buraco):
    """
    Desenha o estado atual do tabuleiro na tela.
    """
    for linha in range(len(tabuleiro_visivel)):
        for coluna in range(len(tabuleiro_visivel[0])):
            x = coluna * lado_celula
            y = linha * lado_celula

            # Desenha a grade do tabuleiro
            retangulo_celula = pygame.Rect(x, y, lado_celula, lado_celula)
            pygame.draw.rect(tela, cores.preto, retangulo_celula, 1)

            # Se a célula já foi revelada
            if tabuleiro_visivel[linha][coluna]:
                conteudo = tabuleiro_solucao[linha][coluna]
                
                # Calcula o ponto central da célula atual
                centro_celula = (x + lado_celula // 2, y + lado_celula // 2)

                if conteudo == 'T':
                    # --- CORREÇÃO PARA O TESOURO ---
                    # Pega o retângulo da imagem e o posiciona no centro da célula
                    pos_imagem = img_tesouro.get_rect(center=centro_celula)
                    tela.blit(img_tesouro, pos_imagem)

                elif conteudo == 'B':
                    # --- CORREÇÃO PARA O BURACO ---
                    # Pega o retângulo da imagem e o posiciona no centro da célula
                    pos_imagem = img_buraco.get_rect(center=centro_celula)
                    tela.blit(img_buraco, pos_imagem)
                    
                else: # É um número
                    # --- O CÓDIGO PARA O TEXTO JÁ ESTAVA CORRETO ---
                    # Apenas removemos o comentário TODO
                    texto = fonte.render(conteudo, True, cores.preto)
                    pos_texto = texto.get_rect(center=centro_celula)
                    tela.blit(texto, pos_texto)
            else:
                # Pinta a célula não revelada com uma cor
                pygame.draw.rect(tela, cores.cinza, retangulo_celula)


# --- Função Principal ---

def main():
    pygame.init()

    # --- Constantes e Configurações ---
    LADO_CELULA = 80
    NUM_LINHAS = 4
    NUM_COLUNAS = 4
    
    # O projeto define 6 tesouros e 3 buracos
    NUM_TESOUROS = 6
    NUM_BURACOS = 3

    # Define o tamanho da tela. Deixamos um espaço extra na parte de baixo para o placar.
    largura_tela = NUM_COLUNAS * LADO_CELULA
    altura_tela = (NUM_LINHAS + 1) * LADO_CELULA
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Caça ao Tesouro")

    # Fontes
    fonte_jogo = pygame.font.SysFont("Arial", 40)
    fonte_placar = pygame.font.SysFont("Arial", 24)

    # Carregando imagens (coloque-as na pasta 'recursos')
    try:
        img_tesouro = pygame.image.load('recursos/tesouro.png')
        img_tesouro = pygame.transform.scale(img_tesouro, (LADO_CELULA - 10, LADO_CELULA - 10))
        
        img_buraco = pygame.image.load('recursos/buraco.png')
        img_buraco = pygame.transform.scale(img_buraco, (LADO_CELULA - 10, LADO_CELULA - 10))
    except pygame.error as e:
        print(f"Erro ao carregar imagens: {e}")
        print("Certifique-se que as imagens 'tesouro.png' e 'buraco.png' estão na pasta 'recursos'.")
        return # Encerra o jogo se não encontrar as imagens

    # --- Variáveis de Estado do Jogo ---
    tabuleiro_solucao = inicializar_tabuleiro(NUM_LINHAS, NUM_COLUNAS, NUM_TESOUROS, NUM_BURACOS)
    tabuleiro_visivel = [[False for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)]
    
    pontos_j1 = 0
    pontos_j2 = 0
    jogador_da_vez = 1
    celulas_reveladas = 0
    total_celulas = NUM_LINHAS * NUM_COLUNAS
    
    jogo_ativo = True
    fim_de_jogo = False
    mensagem_final = ""

    # --- Loop Principal do Jogo ---
    while jogo_ativo:
        # --- Tratamento de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False

            # Ignora cliques se o jogo já terminou
            if fim_de_jogo:
                continue

            # Evento de clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                
                # Converte a coordenada do mouse para índice da matriz
                coluna_clicada = mouse_x // LADO_CELULA
                linha_clicada = mouse_y // LADO_CELULA

                # Verifica se o clique foi dentro do tabuleiro e em uma célula não revelada
                if 0 <= linha_clicada < NUM_LINHAS and not tabuleiro_visivel[linha_clicada][coluna_clicada]:
                    
                    tabuleiro_visivel[linha_clicada][coluna_clicada] = True
                    celulas_reveladas += 1
                    
                    conteudo = tabuleiro_solucao[linha_clicada][coluna_clicada]
                    
                    # Atualiza a pontuação
                    if conteudo == 'T':
                        if jogador_da_vez == 1:
                            pontos_j1 += 100
                        else:
                            pontos_j2 += 100
                    elif conteudo == 'B':
                        if jogador_da_vez == 1:
                            pontos_j1 = max(0, pontos_j1 - 50) # Garante que a pontuação não fica negativa
                        else:
                            pontos_j2 = max(0, pontos_j2 - 50)
                    
                    # Troca o jogador
                    jogador_da_vez = 2 if jogador_da_vez == 1 else 1

                    # Verifica se o jogo terminou
                    if celulas_reveladas == total_celulas:
                        fim_de_jogo = True
                        if pontos_j1 > pontos_j2:
                            mensagem_final = "Jogador 1 Venceu!"
                        elif pontos_j2 > pontos_j1:
                            mensagem_final = "Jogador 2 Venceu!"
                        else:
                            mensagem_final = "Empate!"

        # --- Lógica de Desenho ---
        tela.fill(cores.branco) # Limpa a tela
        
        # Desenha o tabuleiro
        desenhar_tabuleiro(tela, tabuleiro_visivel, tabuleiro_solucao, LADO_CELULA, fonte_jogo, img_tesouro, img_buraco)
        
        # Desenha a área do placar
        area_placar = pygame.Rect(0, NUM_LINHAS * LADO_CELULA, largura_tela, LADO_CELULA)
        pygame.draw.rect(tela, cores.azul_claro, area_placar)
        
        placar_txt = f"J1: {pontos_j1} pontos | J2: {pontos_j2} pontos"
        texto_placar = fonte_placar.render(placar_txt, True, cores.preto)
        tela.blit(texto_placar, (15, NUM_LINHAS * LADO_CELULA + 10))

        if not fim_de_jogo:
            vez_txt = f"Vez do Jogador: {jogador_da_vez}"
            texto_vez = fonte_placar.render(vez_txt, True, cores.preto)
            tela.blit(texto_vez, (15, NUM_LINHAS * LADO_CELULA + 40))
        else:
            texto_final = fonte_placar.render(mensagem_final, True, cores.vermelho)
            tela.blit(texto_final, (largura_tela / 2 - texto_final.get_width() / 2, NUM_LINHAS * LADO_CELULA + 25))

        # Atualiza a tela
        pygame.display.update()

    pygame.quit()

# Executa a função principal
if __name__ == "__main__":
    main()