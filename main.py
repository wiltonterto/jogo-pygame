import pygame
import random
import cores
import menu_inicial 
import config # Importa as configurações dinâmicas (TAMANHO_TABULEIRO, SOM_LIGADO)

# --- Constantes de Configuração Geral (NOVOS VALORES) ---
LARGURA_TELA = 825 
ALTURA_TELA = 660 
LADO_CELULA = 75 

NUM_TESOUROS = 6 
NUM_BURACOS = 3 

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
                      img_tesouro, img_buraco, img_celula_fechada, img_numeros, offset_x, offset_y):
    """Desenha o estado atual do tabuleiro na tela."""
    for linha in range(len(tabuleiro_visivel)):
        for coluna in range(len(tabuleiro_visivel[0])):
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


def desenhar_texto_centralizado(tela, texto, fonte, cor, centro_x, centro_y):
    """Função auxiliar para desenhar texto de forma simplificada."""
    texto_render = fonte.render(texto, True, cor)
    retangulo_texto = texto_render.get_rect(center=(centro_x, centro_y))
    tela.blit(texto_render, retangulo_texto)


def desenhar_tela_fim_jogo(tela, img_fundo, mensagem, fonte_titulo, fonte_botoes, 
                           btn_nova_rodada, btn_voltar, msg_btn_1, msg_btn_2, cor_destaque, cor_normal):
    """Desenha a tela de Game Over/Transição com botões com efeito hover."""
    tela.blit(img_fundo, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # 1. Desenha o título (Mensagem Central)
    desenhar_texto_centralizado(tela, mensagem, fonte_titulo, cor_normal, 
                                LARGURA_TELA / 2, ALTURA_TELA / 2 - 50)

    # 2. Botão 1 (Nova Rodada / Novo Jogo)
    cor_btn_1 = cor_destaque if btn_nova_rodada.collidepoint((mouse_x, mouse_y)) else cor_normal
    desenhar_texto_centralizado(tela, msg_btn_1, fonte_botoes, cor_btn_1, 
                                btn_nova_rodada.centerx, btn_nova_rodada.centery)

    # 3. Botão 2 (Voltar ao Menu)
    cor_btn_2 = cor_destaque if btn_voltar.collidepoint((mouse_x, mouse_y)) else cor_normal
    desenhar_texto_centralizado(tela, msg_btn_2, fonte_botoes, cor_btn_2, 
                                btn_voltar.centerx, btn_voltar.centery)

# --- Função Principal ---

def main():
    pygame.init()
    pygame.mixer.init() 
    
    # --- 1. Inicialização da Tela ---
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Caça ao Tesouro")
    
    # --- 2. Carregamento de Fontes ---
    CAMINHO_FONTE = 'recursos/stitch.ttf' 
    FONTE_FALLBACK = "Arial" 

    try:
        fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 40)
        fonte_botoes = pygame.font.Font(CAMINHO_FONTE, 20)
        fonte_placar = pygame.font.Font(CAMINHO_FONTE, 20)
    except (FileNotFoundError, pygame.error):
        fonte_titulo = pygame.font.SysFont(FONTE_FALLBACK, 40, bold=True)
        fonte_botoes = pygame.font.SysFont(FONTE_FALLBACK, 20)
        fonte_placar = pygame.font.SysFont(FONTE_FALLBACK, 20)
    
    # --- 3. Carregamento de Imagens de Fundo (Menu e Ajustes) ---
    IMG_FUNDO_MENU = None
    IMG_FUNDO_AJUSTES = None
    IMG_FUNDO_JOGO = None 
    IMG_GAME_OVER = None 
    
    try:
        IMG_FUNDO_MENU = pygame.image.load('recursos/tela_inicial.png').convert()
        IMG_FUNDO_AJUSTES = pygame.image.load('recursos/ajustes.png').convert()
        IMG_FUNDO_JOGO = pygame.image.load('recursos/fundo_tabuleiro.png').convert() 
        IMG_GAME_OVER = pygame.image.load('recursos/game_over.png').convert_alpha() 
        
        # Garante o redimensionamento para a tela (825x660)
        if IMG_FUNDO_MENU.get_size() != (LARGURA_TELA, ALTURA_TELA):
            IMG_FUNDO_MENU = pygame.transform.scale(IMG_FUNDO_MENU, (LARGURA_TELA, ALTURA_TELA))
        if IMG_FUNDO_AJUSTES.get_size() != (LARGURA_TELA, ALTURA_TELA):
            IMG_FUNDO_AJUSTES = pygame.transform.scale(IMG_FUNDO_AJUSTES, (LARGURA_TELA, ALTURA_TELA))
        if IMG_FUNDO_JOGO.get_size() != (LARGURA_TELA, ALTURA_TELA):
            IMG_FUNDO_JOGO = pygame.transform.scale(IMG_FUNDO_JOGO, (LARGURA_TELA, ALTURA_TELA))
        if IMG_GAME_OVER.get_size() != (LARGURA_TELA, ALTURA_TELA):
            IMG_GAME_OVER = pygame.transform.scale(IMG_GAME_OVER, (LARGURA_TELA, ALTURA_TELA))

    except (FileNotFoundError, pygame.error) as e:
        print(f"Erro ao carregar imagem de fundo/game over: {e}. Verifique a pasta 'recursos'.")
        # Fallback de tela branca
        IMG_FUNDO_MENU = IMG_FUNDO_AJUSTES = IMG_FUNDO_JOGO = IMG_GAME_OVER = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        IMG_FUNDO_MENU.fill(cores.branco)


    # --- 4. Chamada da tela de menu ---
    modo_jogo = menu_inicial.tela_de_menu(
        tela, LARGURA_TELA, ALTURA_TELA, 
        fonte_titulo, fonte_botoes, 
        IMG_FUNDO_MENU,          
        IMG_FUNDO_AJUSTES      
    )

    if modo_jogo is None or modo_jogo == 'sair':
        pygame.quit()
        return

    # --- 5. Configuração do Tabuleiro ---
    NUM_LINHAS = config.MAPA_TAMANHOS[config.TAMANHO_TABULEIRO][0] 
    NUM_COLUNAS = config.MAPA_TAMANHOS[config.TAMANHO_TABULEIRO][1] 

    TAMANHO_TABULEIRO = NUM_COLUNAS * LADO_CELULA

    # --- CÁLCULO DE OFFSET ADAPTÁVEL PARA CENTRALIZAÇÃO ---
    CENTRO_TELA_X = LARGURA_TELA // 2
    OFFSET_X = CENTRO_TELA_X - (TAMANHO_TABULEIRO // 2)
    BASE_OFFSET_Y = 196 
    TAMANHO_PADRAO_4X4 = 4 * LADO_CELULA
    OFFSET_Y = BASE_OFFSET_Y - (TAMANHO_TABULEIRO - TAMANHO_PADRAO_4X4) // 2

    # --- Carregando Imagens do Jogo ---
    img_tesouro = None
    img_buraco = None
    img_celula_fechada = None
    img_numeros = {}
    
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
    # CRIAÇÃO CORRETA DA MATRIZ
    tabuleiro_visivel = [[False for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)] 
    
    pontos_j1 = 0 
    pontos_j2 = 0 
    jogador_da_vez = 1
    celulas_reveladas = 0
    total_celulas = NUM_LINHAS * NUM_COLUNAS
    
    jogo_ativo = True
    fim_de_jogo = False
    mensagem_final = ""

    # --- Variáveis para Transição de Rodada e Melhor de 3 ---
    fim_da_rodada = False 
    mensagem_rodada = ""
    RODADAS_TOTAL = 3 
    rodada_atual = 1 
    vitorias_j1 = 0
    vitorias_j2 = 0
    
    # --- Definição dos Retângulos dos Botões Finais ---
    LARGURA_BOTAO = 250
    ALTURA_BOTAO = 50
    CENTRO_X = LARGURA_TELA // 2
    
    y_nova_rodada = ALTURA_TELA // 2 + 170 
    y_voltar_menu = ALTURA_TELA // 2 + 238 
    
    botao_nova_rodada = pygame.Rect(CENTRO_X - LARGURA_BOTAO // 2, y_nova_rodada, LARGURA_BOTAO, ALTURA_BOTAO)
    botao_voltar_menu = pygame.Rect(CENTRO_X - LARGURA_BOTAO // 2, y_voltar_menu, LARGURA_BOTAO, ALTURA_BOTAO)
    
    # Cores
    VERDE_DESTAQUE = (0, 179, 0) # Cor de destaque (hover)
    
    # --- Loop Principal do Jogo ---
    while jogo_ativo:
        mouse_pos = pygame.mouse.get_pos()
        
        # --- Tratamento de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False

            # --- Lógica de Botões na Tela de Fim de Jogo ou Fim de Rodada ---
            if fim_de_jogo or fim_da_rodada:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    
                    # 1. Botão VOLTAR AO MENU 
                    if botao_voltar_menu.collidepoint(evento.pos):
                        modo_jogo = menu_inicial.tela_de_menu(
                            tela, LARGURA_TELA, ALTURA_TELA, 
                            fonte_titulo, fonte_botoes, 
                            IMG_FUNDO_MENU,          
                            IMG_FUNDO_AJUSTES
                        )
                        if modo_jogo is None or modo_jogo == 'sair':
                            pygame.quit()
                            return
                        
                        # --- CÓDIGO DE RESET COMPLETO ---
                        pontos_j1 = pontos_j2 = 0
                        celulas_reveladas = 0
                        fim_de_jogo = fim_da_rodada = False
                        vitorias_j1 = vitorias_j2 = 0
                        rodada_atual = 1
                        
                        # Recalcula e recria o tabuleiro (tamanho pode ter mudado no menu)
                        NUM_LINHAS = config.MAPA_TAMANHOS[config.TAMANHO_TABULEIRO][0] 
                        NUM_COLUNAS = config.MAPA_TAMANHOS[config.TAMANHO_TABULEIRO][1] 
                        total_celulas = NUM_LINHAS * NUM_COLUNAS
                        tabuleiro_solucao = inicializar_tabuleiro(NUM_LINHAS, NUM_COLUNAS, NUM_TESOUROS, NUM_BURACOS)
                        # CRIAÇÃO CORRETA DA MATRIZ:
                        tabuleiro_visivel = [[False for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)]
                        jogador_da_vez = 1
                        
                    # 2. Botão NOVA RODADA / NOVO JOGO 
                    if botao_nova_rodada.collidepoint(evento.pos):
                        
                        if modo_jogo == menu_inicial.MODO_MELHOR_DE_3 and fim_da_rodada:
                            # Próxima Rodada (Melhor de 3)
                            
                            if rodada_atual <= RODADAS_TOTAL: 
                                # Reset da RODADA 
                                tabuleiro_solucao = inicializar_tabuleiro(NUM_LINHAS, NUM_COLUNAS, NUM_TESOUROS, NUM_BURACOS)
                                # CRIAÇÃO CORRETA DA MATRIZ:
                                tabuleiro_visivel = [[False for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)] 
                                celulas_reveladas = 0 
                                pontos_j1 = 0 
                                pontos_j2 = 0 
                                jogador_da_vez = 1
                                fim_da_rodada = False # Volta para o jogo normal
                            else:
                                # Fim de Jogo (Melhor de 3 - tela final)
                                fim_da_rodada = False
                                fim_de_jogo = True 
                                
                        elif fim_de_jogo: 
                            # Novo Jogo (Qualquer modo)
                            pontos_j1 = pontos_j2 = 0
                            celulas_reveladas = 0
                            fim_de_jogo = False
                            
                            # Resetar Melhor de 3 (se o modo for o mesmo)
                            vitorias_j1 = vitorias_j2 = 0
                            rodada_atual = 1
                            
                            tabuleiro_solucao = inicializar_tabuleiro(NUM_LINHAS, NUM_COLUNAS, NUM_TESOUROS, NUM_BURACOS)
                            # CRIAÇÃO CORRETA DA MATRIZ:
                            tabuleiro_visivel = [[False for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)]
                            jogador_da_vez = 1
                
                # Interrompe o loop de eventos para evitar cliques no tabuleiro
                if fim_de_jogo or fim_da_rodada:
                    continue


            # --- Bloco de Clique nas Células do Tabuleiro (Lógica do Jogo) ---
            if not fim_de_jogo and not fim_da_rodada and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                coluna_clicada = (mouse_x - OFFSET_X) // LADO_CELULA
                linha_clicada = (mouse_y - OFFSET_Y) // LADO_CELULA

                if (0 <= linha_clicada < NUM_LINHAS and 
                    0 <= coluna_clicada < NUM_COLUNAS and 
                    not tabuleiro_visivel[linha_clicada][coluna_clicada]):
                    
                    tabuleiro_visivel[linha_clicada][coluna_clicada] = True
                    conteudo = tabuleiro_solucao[linha_clicada][coluna_clicada]

                    # --- LÓGICA DE PONTUAÇÃO ÚNICA ---
                    if modo_jogo == menu_inicial.MODO_MELHOR_DE_3 or modo_jogo == menu_inicial.MODO_PADRAO:
                        
                        celulas_reveladas += 1
                        
                        if conteudo == 'T':
                            pontos_j1 += 100 if jogador_da_vez == 1 else 0
                            pontos_j2 += 100 if jogador_da_vez == 2 else 0
                        elif conteudo == 'B':
                            pontos_j1 = max(0, pontos_j1 - 50) if jogador_da_vez == 1 else pontos_j1
                            pontos_j2 = max(0, pontos_j2 - 50) if jogador_da_vez == 2 else pontos_j2
                            
                        jogador_da_vez = 2 if jogador_da_vez == 1 else 1

                        # --- Fim de Rodada/Jogo ---
                        if celulas_reveladas == total_celulas:
                            
                            if modo_jogo == menu_inicial.MODO_MELHOR_DE_3:
                                vencedor = 0
                                if pontos_j1 > pontos_j2:
                                    vitorias_j1 += 1
                                    vencedor = 1
                                elif pontos_j2 > pontos_j1:
                                    vitorias_j2 += 1
                                    vencedor = 2
                                
                                if rodada_atual < RODADAS_TOTAL:
                                    # É FIM DE RODADA, ATIVA TELA DE TRANSIÇÃO
                                    if vencedor > 0:
                                        mensagem_rodada = f"Rodada {rodada_atual} | Jogador {vencedor} VENCEU!"
                                    else:
                                        mensagem_rodada = f"Rodada {rodada_atual} | EMPATE!"
                                    
                                    fim_da_rodada = True
                                    rodada_atual += 1 # Prepara para a próxima rodada
                                else: 
                                    # Fim da PARTIDA (Rodada atual é a última)
                                    fim_de_jogo = True
                                    if vitorias_j1 > vitorias_j2:
                                        mensagem_final = f"JOGADOR 1 VENCEU {vitorias_j1}x{vitorias_j2}!"
                                    elif vitorias_j2 > vitorias_j1:
                                        mensagem_final = f"JOGADOR 2 VENCEU {vitorias_j2}x{vitorias_j1}!"
                                    else:
                                        mensagem_final = f"EMPATE GERAL! {vitorias_j1}x{vitorias_j2}"
                            
                            elif modo_jogo == menu_inicial.MODO_PADRAO:
                                fim_de_jogo = True
                                mensagem_final = "EMPATE!"
                                if pontos_j1 > pontos_j2: mensagem_final = "JOGADOR 1 VENCEU!"
                                elif pontos_j2 > pontos_j1: mensagem_final = "JOGADOR 2 VENCEU!"
                                
                    # --- LÓGICA DO MODO MORTE SÚBITA ---
                    elif modo_jogo == menu_inicial.MODO_MORTE_SUBITA:
                        if conteudo == 'B' or conteudo == 'T':
                            fim_de_jogo = True 
                            if conteudo == 'B':
                                mensagem_final = f"JOGADOR {jogador_da_vez} CAIU NO BURACO! FIM DE JOGO!"
                            else:
                                pontos_j1 += 100 if jogador_da_vez == 1 else 0
                                pontos_j2 += 100 if jogador_da_vez == 2 else 0
                                mensagem_final = f"JOGADOR {jogador_da_vez} VENCEU!"
                        else: 
                            jogador_da_vez = 2 if jogador_da_vez == 1 else 1


        # --- Lógica de Desenho ---
        
        # 1. Desenha o Fundo e o Tabuleiro
        tela.blit(IMG_FUNDO_JOGO, (0, 0))
        desenhar_tabuleiro(tela, tabuleiro_visivel, tabuleiro_solucao, LADO_CELULA, 
                            img_tesouro, img_buraco, img_celula_fechada, img_numeros,
                            OFFSET_X, OFFSET_Y) 

        # 2. Desenho do HUD (Placar e Vez)
        POS_SCORE_J1 = (120, 380) 
        POS_J1_Vez = (165, 105) 
        POS_SCORE_J2 = (695, 380) 
        POS_J2_Vez = (660, 105) 
        
        # O placar exibe a pontuação da rodada atual (pontos_j1/j2)
        desenhar_texto_centralizado(tela, f"{pontos_j1} PTS", fonte_placar, cores.preto, POS_SCORE_J1[0], POS_SCORE_J1[1])
        desenhar_texto_centralizado(tela, f"{pontos_j2} PTS", fonte_placar, cores.preto, POS_SCORE_J2[0], POS_SCORE_J2[1])

        # Desenha o Indicador de Vez (oculta se o jogo/rodada estiver parado)
        cor_j1 = VERDE_DESTAQUE if jogador_da_vez == 1 and not (fim_de_jogo or fim_da_rodada) else cores.preto
        cor_j2 = VERDE_DESTAQUE if jogador_da_vez == 2 and not (fim_de_jogo or fim_da_rodada) else cores.preto

        desenhar_texto_centralizado(tela, "Play 1", fonte_botoes, cor_j1, POS_J1_Vez[0], POS_J1_Vez[1])
        desenhar_texto_centralizado(tela, "Play 2", fonte_botoes, cor_j2, POS_J2_Vez[0], POS_J2_Vez[1])

        # --- 3. Desenho das Telas de Transição / Fim ---
        if fim_de_jogo or fim_da_rodada:
            
            mensagem_a_exibir = mensagem_rodada if fim_da_rodada else mensagem_final
            
            # Controle das mensagens dos botões
            if modo_jogo == menu_inicial.MODO_MELHOR_DE_3 and fim_da_rodada and rodada_atual <= RODADAS_TOTAL:
                # Transição: Próxima Rodada (Aparece após a rodada 1 e 2)
                msg_btn_1 = "Próxima Rodada"
            else:
                # Final: Novo Jogo (Qualquer modo ou Melhor de 3 Final)
                msg_btn_1 = "Novo Jogo"
            
            msg_btn_2 = "Voltar ao Menu"
            
            desenhar_tela_fim_jogo(
                tela, IMG_GAME_OVER, 
                mensagem_a_exibir, 
                fonte_titulo, fonte_botoes, 
                botao_nova_rodada, 
                botao_voltar_menu, 
                msg_btn_1, 
                msg_btn_2, 
                VERDE_DESTAQUE,
                cores.preto # Cor normal dos botões
            )


        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()