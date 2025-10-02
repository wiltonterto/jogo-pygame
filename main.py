import pygame
import random
import cores
import menu_inicial 
import config # Importa as configurações dinâmicas (TAMANHO_TABULEIRO, SOM_LIGADO)

# --- Constantes de Configuração Geral ---
LARGURA_TELA = 1050
ALTURA_TELA = 840 
LADO_CELULA = 100 # Tamanho base da célula (usado para 4x4, 6x6, 8x8)

NUM_TESOUROS = 6 # Mantido constante
NUM_BURACOS = 3 # Mantido constante

# --- Funções Auxiliares (Sem Alterações) ---
def inicializar_tabuleiro(linhas, colunas, num_tesouros, num_buracos):
    """
    Cria o tabuleiro do jogo, distribui os tesouros e buracos,
    e calcula os números das casas vizinhas.
    """
    # ... (Seu código da função inicializar_tabuleiro permanece inalterado) ...
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
                      img_tesouro, img_buraco, img_celula_fechada, img_numeros, offset_x, offset_y):
    """
    Desenha o estado atual do tabuleiro na tela, aplicando o offset para centralização.
    """
    for linha in range(len(tabuleiro_visivel)):
        for coluna in range(len(tabuleiro_visivel[0])):
            # Posicionamento ajustado pelo offset
            x = coluna * lado_celula + offset_x 
            y = linha * lado_celula + offset_y

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
            # O desenho da borda da célula foi removido para usar o visual do fundo


def desenhar_texto_centralizado(tela, texto, fonte, cor, centro_x, centro_y):
    """Função auxiliar para desenhar texto de forma simplificada."""
    texto_render = fonte.render(texto, True, cor)
    retangulo_texto = texto_render.get_rect(center=(centro_x, centro_y))
    tela.blit(texto_render, retangulo_texto)


# --- Função Principal ---

def main():
    pygame.init()
    pygame.mixer.init() # Garante que o som inicialize (para futuras implementações)
    
    # --- 1. Inicialização da Tela ---
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Caça ao Tesouro")
    
    # --- 2. Carregamento de Fontes ---
    CAMINHO_FONTE = 'recursos/stitch.ttf' 
    FONTE_FALLBACK = "Arial" 

    try:
        fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 60)
        fonte_botoes = pygame.font.Font(CAMINHO_FONTE, 30)
        fonte_placar = pygame.font.Font(CAMINHO_FONTE, 24)
    except (FileNotFoundError, pygame.error):
        fonte_titulo = pygame.font.SysFont(FONTE_FALLBACK, 60, bold=True)
        fonte_botoes = pygame.font.SysFont(FONTE_FALLBACK, 30)
        fonte_placar = pygame.font.SysFont(FONTE_FALLBACK, 24)
    
    # --- 3. Carregamento de Imagens de Fundo (Menu e Ajustes) ---
    IMG_FUNDO_MENU = None
    IMG_FUNDO_AJUSTES = None
    IMG_FUNDO_JOGO = None # <-- NOVO
    
    try:
        IMG_FUNDO_MENU = pygame.image.load('recursos/tela_inicial.png').convert()
        IMG_FUNDO_AJUSTES = pygame.image.load('recursos/ajustes.png').convert()
        IMG_FUNDO_JOGO = pygame.image.load('recursos/fundo_tabuleiro.png').convert() # <-- CARREGAMENTO AQUI!
        
        # Garante o redimensionamento para a tela (1050x840)
        if IMG_FUNDO_MENU.get_size() != (LARGURA_TELA, ALTURA_TELA):
            IMG_FUNDO_MENU = pygame.transform.scale(IMG_FUNDO_MENU, (LARGURA_TELA, ALTURA_TELA))
        if IMG_FUNDO_AJUSTES.get_size() != (LARGURA_TELA, ALTURA_TELA):
            IMG_FUNDO_AJUSTES = pygame.transform.scale(IMG_FUNDO_AJUSTES, (LARGURA_TELA, ALTURA_TELA))
        if IMG_FUNDO_JOGO.get_size() != (LARGURA_TELA, ALTURA_TELA): # <-- NOVO
            IMG_FUNDO_JOGO = pygame.transform.scale(IMG_FUNDO_JOGO, (LARGURA_TELA, ALTURA_TELA))

    except (FileNotFoundError, pygame.error) as e:
        print(f"Erro ao carregar imagem de fundo: {e}. Verifique a pasta 'recursos'.")
        # Fallback de tela branca
        IMG_FUNDO_MENU = IMG_FUNDO_AJUSTES = IMG_FUNDO_JOGO = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        IMG_FUNDO_MENU.fill(cores.branco)


    # --- 4. Chamada da tela de menu (Passando as duas imagens) ---
    modo_jogo = menu_inicial.tela_de_menu(
        tela, LARGURA_TELA, ALTURA_TELA, 
        fonte_titulo, fonte_botoes, 
        IMG_FUNDO_MENU,          
        IMG_FUNDO_AJUSTES       
    )

    if modo_jogo is None or modo_jogo == 'sair':
        pygame.quit()
        return

    # --- 5. Configuração do Tabuleiro (Lendo do config.py) ---
    # Lendo o tamanho do tabuleiro definido no menu de Ajustes (config.py)
    NUM_LINHAS = config.MAPA_TAMANHOS[config.TAMANHO_TABULEIRO][0] 
    NUM_COLUNAS = config.MAPA_TAMANHOS[config.TAMANHO_TABULEIRO][1] 

    # O tamanho do tabuleiro muda se o jogador escolher 6x6 ou 8x8
    TAMANHO_TABULEIRO = NUM_COLUNAS * LADO_CELULA

    # Offset para centralizar o tabuleiro na área de vidro fosco (4x4)
    # Se o tamanho mudar para 6x6 ou 8x8, o tabuleiro ainda começa aqui!
    OFFSET_X = 325 
    OFFSET_Y = 280 
    
    # --- Carregando Imagens do Jogo (Tesouros, Buracos, Números) ---
    img_tesouro = None
    img_buraco = None
    img_celula_fechada = None
    img_numeros = {}
    
    # ... (Seu código de carregamento de imagens de jogo, ajustado para LADO_CELULA=100) ...
    try:
        img_tesouro = pygame.transform.scale(pygame.image.load('recursos/tesouro.JPG'), (LADO_CELULA, LADO_CELULA))
        img_buraco = pygame.transform.scale(pygame.image.load('recursos/buraco.JPG'), (LADO_CELULA, LADO_CELULA))
        img_celula_fechada = pygame.transform.scale(pygame.image.load('recursos/celula_fechada.JPG'), (LADO_CELULA, LADO_CELULA))

        nomes_numeros = {'0': 'zero', '1': 'um', '2': 'dois', '3': 'tres', '4': 'quatro'}
        for numero, nome_arquivo in nomes_numeros.items():
            img_numeros[numero] = pygame.transform.scale(pygame.image.load(f'recursos/{nome_arquivo}.JPG'), (LADO_CELULA, LADO_CELULA))

    except (FileNotFoundError, pygame.error) as e:
        print(f"Erro ao carregar imagem de jogo: {e}. O jogo será encerrado.")
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
                
                # Ajusta a posição do clique para as coordenadas do tabuleiro
                coluna_clicada = (mouse_x - OFFSET_X) // LADO_CELULA
                linha_clicada = (mouse_y - OFFSET_Y) // LADO_CELULA

                # Garante que o clique está dentro do tabuleiro e a célula está fechada
                if (0 <= linha_clicada < NUM_LINHAS and 
                    0 <= coluna_clicada < NUM_COLUNAS and 
                    not tabuleiro_visivel[linha_clicada][coluna_clicada]):
                    
                    tabuleiro_visivel[linha_clicada][coluna_clicada] = True
                    conteudo = tabuleiro_solucao[linha_clicada][coluna_clicada]
                    
                    # Lógica para o modo Padrão / Morte Súbita ...
                    # ... (Essa lógica permanece a mesma) ...
                    if modo_jogo == menu_inicial.MODO_PADRAO or modo_jogo == menu_inicial.MODO_MELHOR_DE_3:
                        celulas_reveladas += 1
                        if conteudo == 'T':
                            pontos_j1 += 100 if jogador_da_vez == 1 else 0
                            pontos_j2 += 100 if jogador_da_vez == 2 else 0
                        elif conteudo == 'B':
                            pontos_j1 = max(0, pontos_j1 - 50) if jogador_da_vez == 1 else pontos_j1
                            pontos_j2 = max(0, pontos_j2 - 50) if jogador_da_vez == 2 else pontos_j2
                        
                        # Troca de jogador
                        jogador_da_vez = 2 if jogador_da_vez == 1 else 1
                        
                        if celulas_reveladas == total_celulas:
                            fim_de_jogo = True
                            mensagem_final = "Empate!"
                            if pontos_j1 > pontos_j2: mensagem_final = "Jogador 1 Venceu!"
                            elif pontos_j2 > pontos_j1: mensagem_final = "Jogador 2 Venceu!"

                    elif modo_jogo == menu_inicial.MODO_MORTE_SUBITA:
                        if conteudo == 'B':
                            fim_de_jogo = True
                            mensagem_final = f"Jogador {jogador_da_vez} caiu no buraco! Fim de Jogo!"
                        elif conteudo == 'T':
                            fim_de_jogo = True
                            pontos_j1 += 100 if jogador_da_vez == 1 else 0
                            pontos_j2 += 100 if jogador_da_vez == 2 else 0
                            mensagem_final = f"Jogador {jogador_da_vez} Venceu!"
                        else: # Se for um número, apenas troca o jogador e continua
                            jogador_da_vez = 2 if jogador_da_vez == 1 else 1


        # --- Lógica de Desenho ---
        
        # 1. Desenha o Fundo do Jogo (fundo_tabuleiro.png)
        tela.blit(IMG_FUNDO_JOGO, (0, 0))
        
        # 2. Desenha o Tabuleiro com o Offset
        desenhar_tabuleiro(tela, tabuleiro_visivel, tabuleiro_solucao, LADO_CELULA, 
                           img_tesouro, img_buraco, img_celula_fechada, img_numeros,
                           OFFSET_X, OFFSET_Y) 

        # --- 3. Desenho do HUD (Placar e Vez) ---
        
        # Posições no design 7.jpg (centralizadas)
        POS_SCORE_J1 = (220, 500) # Caixa 'score' Esquerda
        POS_J1_Vez = (220, 100) # Botão 'Play 1'
        POS_SCORE_J2 = (830, 500) # Caixa 'score' Direita
        POS_J2_Vez = (830, 100) # Botão 'Play 2'
        
        # Cor de Destaque (Verde)
        VERDE = (0, 255, 0)
        
        # Desenha Placar J1
        desenhar_texto_centralizado(tela, f"{pontos_j1} PTS", fonte_placar, cores.preto, POS_SCORE_J1[0], POS_SCORE_J1[1])
        
        # Desenha Placar J2
        desenhar_texto_centralizado(tela, f"{pontos_j2} PTS", fonte_placar, cores.preto, POS_SCORE_J2[0], POS_SCORE_J2[1])

        # Desenha o Indicador de Vez (muda a cor do texto Play 1/2)
        cor_j1 = VERDE if jogador_da_vez == 1 and not fim_de_jogo else cores.preto
        cor_j2 = VERDE if jogador_da_vez == 2 and not fim_de_jogo else cores.preto

        desenhar_texto_centralizado(tela, "Play 1", fonte_botoes, cor_j1, POS_J1_Vez[0], POS_J1_Vez[1])
        desenhar_texto_centralizado(tela, "Play 2", fonte_botoes, cor_j2, POS_J2_Vez[0], POS_J2_Vez[1])

        # Desenha Mensagem Final (no centro da tela)
        if fim_de_jogo:
            desenhar_texto_centralizado(tela, mensagem_final, fonte_titulo, cores.vermelho, LARGURA_TELA / 2, ALTURA_TELA / 2)


        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()