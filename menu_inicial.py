import pygame
import cores 
import config

# --- Constantes de Modos de Jogo ---
MODO_PADRAO = 'padrao'
MODO_MELHOR_DE_3 = 'melhor_de_3'
MODO_MORTE_SUBITA = 'morte_subita'
MODO_AJUSTES = 'ajustes'   
MODO_REGRAS = 'regras'     
MODO_SAIR = 'sair'         
MODO_RECOMECO = 'recomecar' 

# --- Constantes de Cores para o Hover ---
PRETO = (0, 0, 0) 
VERDE_DESTAQUE = (144, 238, 144) 
COR_TITULO = (30, 30, 30) 
CINZA_CLARO = (220, 220, 220) 

# --- Constantes Visuais para AJUSTES (Proporcionais a 825x660) ---

LARGURA_QUADRADO = 142 
ALTURA_QUADRADO = 142 
ESPACO_QUADRADO = 200 
Y_BOTOES_AJUSTES = 265 

COR_BOTAO_LIGADO = VERDE_DESTAQUE
COR_BOTAO_DESLIGADO = CINZA_CLARO

# --- Funções de Configuração ---

def tela_de_regras(tela, largura_tela, altura_tela, fonte_botoes, cor_normal, cor_destaque):
    """
    Mostra a tela de regras em duas páginas com navegação.
    Retorna 'menu' quando o jogador clica em 'Voltar ao Menu' ou 'sair'.
    """
    
    # 1. Carregamento e Redimensionamento das Imagens (já na pasta 'recursos')
    try:
        # Imagem 1: Regras e Pontuação (Com botão "Próximo")
        img_regras_1 = pygame.image.load('recursos/regras_jogo.png').convert_alpha()
        img_regras_1 = pygame.transform.scale(img_regras_1, (largura_tela, altura_tela))
        
        # Imagem 2: Modos de Jogo (Com botão "Voltar ao Menu")
        img_regras_2 = pygame.image.load('recursos/regras_jogo_1.png').convert_alpha()
        img_regras_2 = pygame.transform.scale(img_regras_2, (largura_tela, altura_tela))

    except pygame.error as e:
        print(f"Erro ao carregar imagens de regras: {e}. Verifique os nomes (regras_jogo.png e regras_jogo_1.png).")
        return MODO_REGRAS # Se falhar, retorna ao menu principal
        
    # 2. Definição do Botão (Posição fixa na parte inferior da sua imagem)
    LARGURA_BOTAO = 190 # Usando a largura padrão de get_botoes_config para consistência
    ALTURA_BOTAO = 42
    CENTRO_X = largura_tela // 2
    
    # Posição Y do botão (Ajustada para o local exato na imagem)
    POS_Y_BOTAO = altura_tela - 136 
    
    botao_acao = pygame.Rect(CENTRO_X - LARGURA_BOTAO // 2, POS_Y_BOTAO, LARGURA_BOTAO, ALTURA_BOTAO)
    
    pagina_atual = 1
    
    # 3. Loop da Tela de Regras
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Desenha o fundo da página atual
        if pagina_atual == 1:
            tela.blit(img_regras_1, (0, 0))
            texto_botao = "PRÓXIMO"
        else: # página_atual == 2
            tela.blit(img_regras_2, (0, 0))
            texto_botao = "VOLTAR AO MENU"
        
        # Lógica do Botão Hover
        cor_btn = cor_destaque if botao_acao.collidepoint((mouse_x, mouse_y)) else cor_normal
        
        # Desenha o texto do botão (usando a função de renderização de texto padrão)
        texto_renderizado = fonte_botoes.render(texto_botao, True, cor_btn)
        tela.blit(texto_renderizado, texto_renderizado.get_rect(center=botao_acao.center))

        # 4. Tratamento de Eventos (Cliques)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_acao.collidepoint(evento.pos):
                    if pagina_atual == 1:
                        # Vai para a página 2
                        pagina_atual = 2
                    else:
                        # Clicou em "Voltar ao Menu" na página 2
                        return MODO_REGRAS # Sinaliza para voltar ao menu principal

        pygame.display.flip()

def get_botoes_config(largura_tela):
    """Define as posições e ações de todos os botões do menu."""
    
    LARGURA_BOTAO = 190 
    ALTURA_BOTAO = 42   
    ESPACO_VERTICAL = 52
    
    # O ponto X onde o retângulo de clique começa (centralizado em 825px)
    x_start = largura_tela // 2 - LARGURA_BOTAO // 2 
    
    # Novo centro vertical é 660 / 2 = 330
    CENTRO_Y = 300 
    
    # Posição do topo do primeiro botão (Ajustado para o novo centro)
    y_start_base = 314
    
    return [
        {'texto': "MODO PADRÃO", 'modo': MODO_PADRAO, 
         'retangulo': pygame.Rect(x_start, y_start_base + 0 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
        
        {'texto': "MELHOR DE 3", 'modo': MODO_MELHOR_DE_3, 
         'retangulo': pygame.Rect(x_start, y_start_base + 1 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
         
        {'texto': "MORTE SÚBITA", 'modo': MODO_MORTE_SUBITA, 
         'retangulo': pygame.Rect(x_start, y_start_base + 2 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},

        {'texto': "AJUSTES", 'modo': MODO_AJUSTES, 
         'retangulo': pygame.Rect(x_start, y_start_base + 3 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},

        {'texto': "REGRAS", 'modo': MODO_REGRAS, 
         'retangulo': pygame.Rect(x_start, y_start_base + 4 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
         
        {'texto': "SAIR", 'modo': MODO_SAIR, 
         'retangulo': pygame.Rect(x_start, y_start_base + 5 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
    ]


# --- Função da Tela de Ajustes (Design 4.png) ---

def tela_de_ajustes(tela, largura_tela, altura_tela, fonte_titulo, fonte_botoes, img_fundo_menu, img_fundo_ajustes):
    
    # 1. Definição dos Retângulos de Clique para AJUSTES
    x_center = largura_tela // 2
    
    # Cálculo para centralizar os 3 botões quadrados
    x_som = x_center - ESPACO_QUADRADO 
    x_6x6 = x_center
    x_8x8 = x_center + ESPACO_QUADRADO
    
    botoes_ajustes = [
        {'texto': "SOM", 'acao': 'som', 
         'retangulo': pygame.Rect(x_som - LARGURA_QUADRADO // 2, Y_BOTOES_AJUSTES, LARGURA_QUADRADO, ALTURA_QUADRADO)},
        
        {'texto': "6X6", 'acao': '6x6', 
         'retangulo': pygame.Rect(x_6x6 - LARGURA_QUADRADO // 2, Y_BOTOES_AJUSTES, LARGURA_QUADRADO, ALTURA_QUADRADO)},
        
        {'texto': "8X8", 'acao': '8x8', 
         'retangulo': pygame.Rect(x_8x8 - LARGURA_QUADRADO // 2, Y_BOTOES_AJUSTES, LARGURA_QUADRADO, ALTURA_QUADRADO)},
    ]
    
    # Botão Voltar (na parte inferior) - Proporcionalmente ajustado
    botao_voltar = pygame.Rect(x_center - 100, altura_tela - 110, 200, 50)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos = evento.pos
                
                # Clique no Botão VOLTAR: Retorna ao menu principal
                if botao_voltar.collidepoint(mouse_pos):
                    return MODO_AJUSTES 
                
                # Lógica de Clique nos Botões de Ajuste
                for botao in botoes_ajustes:
                    if botao['retangulo'].collidepoint(mouse_pos):
                        acao = botao['acao']
                        
                        if acao == 'som':
                            config.SOM_LIGADO = not config.SOM_LIGADO
                            
                        elif acao in ["6x6", "8x8"]:
                            config.TAMANHO_TABULEIRO = acao
                            
        
        # --- Lógica de Desenho ---
        tela.blit(img_fundo_ajustes, (0, 0))
        
        # Desenha os 3 Botões de Ajuste (TOTALMENTE TRANSPARENTES, APENAS O TEXTO REAGE)
        for botao in botoes_ajustes:
            rect = botao['retangulo']
            
            # 1. Verifica o estado de SELEÇÃO PERMANENTE (PARA O CASO DE TER QUE TER UM DESTAQUE)
            esta_selecionado = (botao['acao'] == 'som' and config.SOM_LIGADO) or \
                               (botao['acao'] in ["6x6", "8x8"] and config.TAMANHO_TABULEIRO == botao['acao'])
            
            
            # 2. Lógica de COR do Texto
            cor_texto = PRETO # Cor padrão do texto
            
            if esta_selecionado:
                # O texto deve ser verde se estiver selecionado
                cor_texto = VERDE_DESTAQUE
                
            if rect.collidepoint(mouse_pos):
                # No hover, o texto fica verde (independente da seleção)
                cor_texto = VERDE_DESTAQUE 
                
            
            # NOTA: Removemos todos os pygame.draw.rect(tela, ...) para o preenchimento ou contorno.
            
            
            # 3. Desenha o texto do botão
            texto_render = fonte_botoes.render(botao['texto'], True, cor_texto)
            tela.blit(texto_render, texto_render.get_rect(center=rect.center))


        # --- Desenha o botão VOLTAR (TOTALMENTE TRANSPARENTE, APENAS O TEXTO REAGE) ---
        cor_texto_voltar = PRETO 
        
        # Lógica de HOVER para o botão VOLTAR
        if botao_voltar.collidepoint(mouse_pos):
            cor_texto_voltar = VERDE_DESTAQUE
            
        # NOTA: Removemos os pygame.draw.rect(tela, ...) para o preenchimento ou contorno.
            
        # Desenha o texto (com a cor de hover)
        texto_voltar = fonte_botoes.render("VOLTAR", True, cor_texto_voltar)
        tela.blit(texto_voltar, texto_voltar.get_rect(center=botao_voltar.center))
        
        pygame.display.flip()


# --- Função Principal do Menu ---

def tela_de_menu(tela, largura_tela, altura_tela, fonte_titulo, fonte_botoes, img_fundo_menu, img_fundo_ajustes):
    """
    Exibe a tela de menu inicial, usa a imagem de fundo e gerencia a seleção de modo de jogo.
    """
    botoes_config = get_botoes_config(largura_tela)
    
    while True:
        mouse_pos = pygame.mouse.get_pos() 
        
        # --- Tratamento de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                
                # Verifica qual botão foi clicado
                for botao in botoes_config:
                    if botao['retangulo'].collidepoint((mouse_x, mouse_y)):
                        modo_escolhido = botao['modo']

                        if modo_escolhido == MODO_AJUSTES:
                            # SE CLICAR EM AJUSTES, CHAMA A NOVA TELA
                            resultado_ajustes = tela_de_ajustes(
                                tela, largura_tela, altura_tela, 
                                fonte_titulo, fonte_botoes, 
                                img_fundo_menu,             
                                img_fundo_ajustes           
                            )
                            # Se o usuário fechar a janela (QUIT) na tela de ajustes
                            if resultado_ajustes is None:
                                return None
                            # Se retornar, o loop do menu principal continua
                            
                        elif modo_escolhido == MODO_SAIR:
                            return None 
                            
                        # Para todos os modos de jogo (Padrão, Morte Súbita, Melhor de 3)
                        elif modo_escolhido == MODO_PADRAO or modo_escolhido == MODO_MORTE_SUBITA or modo_escolhido == MODO_MELHOR_DE_3:
                            return modo_escolhido
                            
                        # Para Regras, futuramente você chamaria a tela_de_regras
                        elif modo_escolhido == MODO_REGRAS:
                            # 1. CHAMA A NOVA TELA DE REGRAS
                            resultado_regras = tela_de_regras(tela, largura_tela, altura_tela, fonte_botoes, PRETO, VERDE_DESTAQUE)
                            
                            # 2. Lógica de retorno
                            if resultado_regras is None:
                                return None # Usuário clicou no X (Sair)
                                # Se retornar MODO_REGRAS (Voltar ao Menu), o loop continua e redesenha o menu

                            
                        # O loop principal continua para desenhar o menu novamente
        
        # --- Lógica de Desenho ---
        
        # 1. Desenha o Fundo (Sua imagem de menu principal)
        tela.blit(img_fundo_menu, (0, 0))
        
        # 2. Desenha os Botões e o Efeito Hover
        for botao in botoes_config:
            retangulo = botao['retangulo']
            texto = botao['texto']
            
            # 3.1. Define a Cor do Texto (Lógica de HOVER)
            if retangulo.collidepoint(mouse_pos):
                cor_texto = VERDE_DESTAQUE 
            else:
                cor_texto = PRETO 
            
            # 3.2. Desenha o Texto, centralizado no retângulo invisível
            texto_renderizado = fonte_botoes.render(texto, True, cor_texto)
            tela.blit(texto_renderizado, texto_renderizado.get_rect(center=retangulo.center))
        
        pygame.display.flip()

