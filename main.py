import pygame
import random
import cores
import menu_inicial # Importa o novo módulo

# --- Funções Auxiliares ---
def inicializar_tabuleiro(linhas, colunas, num_tesouros, num_buracos):
    """
    Cria o tabuleiro do jogo, distribui os tesouros e buracos,
    e calcula os números das casas vizinhas.
    """
    tabuleiro = [[0 for _ in range(colunas)] for _ in range(linhas)]

    # Distribui os tesouros ('T') aleatoriamente
    tesouros_plantados = 0
    while tesouros_plantados < num_tesouros:
        l = random.randint(0, linhas - 1)
        c = random.randint(0, colunas - 1)
        if tabuleiro[l][c] == 0:
            tabuleiro[l][c] = 'T'
            tesouros_plantados += 1

    # Distribui os buracos ('B') aleatoriamente
    buracos_plantados = 0
    while buracos_plantados < num_buracos:
        l = random.randint(0, linhas - 1)
        c = random.randint(0, colunas - 1)
        if tabuleiro[l][c] == 0:
            tabuleiro[l][c] = 'B'
            buracos_plantados += 1

    # Calcula os números para as casas restantes
    for l in range(linhas):
        for c in range(colunas):
            if tabuleiro[l][c] == 0:
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
                
                tabuleiro[l][c] = str(vizinhos)
    
    return tabuleiro

def desenhar_tabuleiro(tela, tabuleiro_visivel, tabuleiro_solucao, lado_celula, 
                      img_tesouro, img_buraco, img_celula_fechada, img_numeros):
    """
    Desenha o estado atual do tabuleiro na tela.
    """
    for linha in range(len(tabuleiro_visivel)):
        for coluna in range(len(tabuleiro_visivel[0])):
            x = coluna * lado_celula
            y = linha * lado_celula

            if tabuleiro_visivel[linha][coluna]:
                conteudo = tabuleiro_solucao[linha][coluna]
                
                if conteudo == 'T':
                    tela.blit(img_tesouro, (x, y))
                elif conteudo == 'B':
                    tela.blit(img_buraco, (x, y))
                else:
                    if conteudo in img_numeros:
                        tela.blit(img_numeros[conteudo], (x, y))
            else:
                tela.blit(img_celula_fechada, (x, y))
            
            retangulo_celula = pygame.Rect(x, y, lado_celula, lado_celula)
            pygame.draw.rect(tela, cores.branco, retangulo_celula, 1)


# --- Função Principal ---

def main():
    pygame.init()

    # --- Constantes e Configurações ---
    LADO_CELULA = 120
    NUM_LINHAS = 4
    NUM_COLUNAS = 4
    
    NUM_TESOUROS = 6
    NUM_BURACOS = 3

    largura_tela = NUM_COLUNAS * LADO_CELULA
    altura_tela = (NUM_LINHAS + 1) * LADO_CELULA
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Caça ao Tesouro")

    # Fontes
    fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
    fonte_botoes = pygame.font.SysFont("Arial", 30)
    fonte_placar = pygame.font.SysFont("Arial", 24)
    
    # --- Chamada da tela de menu ---
    modo_jogo = menu_inicial.tela_de_menu(tela, largura_tela, altura_tela, fonte_titulo, fonte_botoes)

    if modo_jogo is None:
        pygame.quit()
        return

    # --- Carregando Imagens ---
    img_tesouro = None
    img_buraco = None
    img_celula_fechada = None
    img_numeros = {}

    try:
        img_tesouro = pygame.image.load('recursos/tesouro.JPG')
        img_buraco = pygame.image.load('recursos/buraco.JPG')
        img_celula_fechada = pygame.image.load('recursos/celula_fechada.JPG')

        img_tesouro = pygame.transform.scale(img_tesouro, (LADO_CELULA, LADO_CELULA))
        img_buraco = pygame.transform.scale(img_buraco, (LADO_CELULA, LADO_CELULA))
        img_celula_fechada = pygame.transform.scale(img_celula_fechada, (LADO_CELULA, LADO_CELULA))

        nomes_numeros = {
            '0': 'zero',
            '1': 'um',
            '2': 'dois',
            '3': 'tres',
            '4': 'quatro'
        }
        
        for numero, nome_arquivo in nomes_numeros.items():
            caminho_arquivo = f'recursos/{nome_arquivo}.JPG'
            img = pygame.image.load(caminho_arquivo)
            img_numeros[numero] = pygame.transform.scale(img, (LADO_CELULA, LADO_CELULA))

    except FileNotFoundError as e:
        print(f"Erro ao carregar imagem: {e}")
        print("Verifique os nomes dos arquivos e a pasta 'recursos'.")
        return
    except pygame.error as e:
        print(f"Erro no Pygame ao carregar/processar imagens: {e}")
        return

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

            if fim_de_jogo:
                continue

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                
                coluna_clicada = mouse_x // LADO_CELULA
                linha_clicada = mouse_y // LADO_CELULA

                if 0 <= linha_clicada < NUM_LINHAS and 0 <= coluna_clicada < NUM_COLUNAS and not tabuleiro_visivel[linha_clicada][coluna_clicada]:
                    
                    tabuleiro_visivel[linha_clicada][coluna_clicada] = True
                    
                    conteudo = tabuleiro_solucao[linha_clicada][coluna_clicada]
                    
                    # Lógica para o modo Padrão
                    if modo_jogo == menu_inicial.MODO_PADRAO or modo_jogo == menu_inicial.MODO_MELHOR_DE_3:
                        celulas_reveladas += 1
                        if conteudo == 'T':
                            if jogador_da_vez == 1:
                                pontos_j1 += 100
                            else:
                                pontos_j2 += 100
                        elif conteudo == 'B':
                            if jogador_da_vez == 1:
                                pontos_j1 = max(0, pontos_j1 - 50)
                            else:
                                pontos_j2 = max(0, pontos_j2 - 50)
                        
                        # Troca de jogador
                        jogador_da_vez = 2 if jogador_da_vez == 1 else 1
                        
                        # Verifica se o jogo no modo padrão terminou
                        if celulas_reveladas == total_celulas:
                            fim_de_jogo = True
                            if pontos_j1 > pontos_j2:
                                mensagem_final = "Jogador 1 Venceu!"
                            elif pontos_j2 > pontos_j1:
                                mensagem_final = "Jogador 2 Venceu!"
                            else:
                                mensagem_final = "Empate!"

                    # Lógica para o modo Morte Súbita
                    elif modo_jogo == menu_inicial.MODO_MORTE_SUBITA:
                        if conteudo == 'B':
                            fim_de_jogo = True
                            mensagem_final = f"Jogador {jogador_da_vez} caiu no buraco! Fim de Jogo!"
                        elif conteudo == 'T':
                            fim_de_jogo = True
                            if jogador_da_vez == 1:
                                pontos_j1 += 100
                                mensagem_final = "Jogador 1 Venceu!"
                            else:
                                pontos_j2 += 100
                                mensagem_final = "Jogador 2 Venceu!"
                        else: # Se for um número, apenas troca o jogador e continua
                            jogador_da_vez = 2 if jogador_da_vez == 1 else 1


        # --- Lógica de Desenho ---
        tela.fill(cores.branco)
        
        desenhar_tabuleiro(tela, tabuleiro_visivel, tabuleiro_solucao, LADO_CELULA, 
                           img_tesouro, img_buraco, img_celula_fechada, img_numeros)
       
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

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()