import pygame
import cores 
import config

# Inicializamos a variável de som como None. Ela será carregada
# mais tarde, dentro da tela_de_menu, após a inicialização do mixer.
SOM_BOTAO_HOVER = None

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
    """
    
    # 1. Carregamento e Redimensionamento das Imagens
    try:
        img_regras_1 = pygame.image.load('recursos/regras_jogo.png').convert_alpha()
        img_regras_1 = pygame.transform.scale(img_regras_1, (largura_tela, altura_tela))
        
        img_regras_2 = pygame.image.load('recursos/regras_jogo_1.png').convert_alpha()
        img_regras_2 = pygame.transform.scale(img_regras_2, (largura_tela, altura_tela))

    except pygame.error as e:
        print(f"Erro ao carregar imagens de regras: {e}. Verifique os nomes.")
        return MODO_REGRAS
        
    # 2. Definição do Botão
    LARGURA_BOTAO = 190 
    ALTURA_BOTAO = 42
    CENTRO_X = largura_tela // 2
    
    POS_Y_BOTAO = altura_tela - 90 
    
    botao_acao = pygame.Rect(CENTRO_X - LARGURA_BOTAO // 2, POS_Y_BOTAO, LARGURA_BOTAO, ALTURA_BOTAO)
    
    pagina_atual = 1
    
    # Rastreamento de hover para o som
    botao_em_hover_anterior = None 
    
    # 3. Loop da Tela de Regras
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_atual_em_hover = None
        
        # Desenha o fundo da página atual
        if pagina_atual == 1:
            tela.blit(img_regras_1, (0, 0))
            texto_botao = "PRÓXIMO"
        else: # página_atual == 2
            tela.blit(img_regras_2, (0, 0))
            texto_botao = "VOLTAR AO MENU"
        
        # Lógica do Botão Hover e Som
        if botao_acao.collidepoint((mouse_x, mouse_y)):
            cor_btn = cor_destaque
            botao_atual_em_hover = botao_acao
        else:
            cor_btn = cor_normal

        # Lógica de tocar o som
        # Adiciona a verificação config.SOM_LIGADO
        if SOM_BOTAO_HOVER is not None and config.SOM_LIGADO: 
            if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                SOM_BOTAO_HOVER.play()
        
        # Desenha o texto do botão
        texto_renderizado = fonte_botoes.render(texto_botao, True, cor_btn)
        tela.blit(texto_renderizado, texto_renderizado.get_rect(center=botao_acao.center))

        # Atualiza o estado de hover
        botao_em_hover_anterior = botao_atual_em_hover
        
        # 4. Tratamento de Eventos (Cliques)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_acao.collidepoint(evento.pos):
                    if pagina_atual == 1:
                        pagina_atual = 2
                    else:
                        return MODO_REGRAS

        pygame.display.flip()

def get_botoes_config(largura_tela):
    """Define as posições e ações de todos os botões do menu."""
    LARGURA_BOTAO = 190 
    ALTURA_BOTAO = 42   
    ESPACO_VERTICAL = 52
    
    x_start = largura_tela // 2 - LARGURA_BOTAO // 2 
    CENTRO_Y = 300 
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


# --- Função da Tela de Ajustes ---

def tela_de_ajustes(tela, largura_tela, altura_tela, fonte_titulo, fonte_botoes, img_fundo_menu, img_fundo_ajustes):
    
    # ... (Definição dos Botões e Constantes - SEM ALTERAÇÃO) ...
    x_center = largura_tela // 2
    
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
    
    botao_voltar = pygame.Rect(x_center - 100, altura_tela - 110, 200, 50)
    
    # Variável que rastreia qual retângulo estava em HOVER no quadro anterior.
    botao_em_hover_anterior = None
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        # Variável que rastreia qual retângulo ESTÁ em HOVER neste quadro.
        botao_atual_em_hover = None 
        
        for evento in pygame.event.get():
            # ... (Lógica de Eventos e Cliques - SEM ALTERAÇÃO) ...
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos_clique = evento.pos
                
                # Clique no Botão VOLTAR
                if botao_voltar.collidepoint(mouse_pos_clique):
                    return MODO_AJUSTES 
                
                # Lógica de Clique nos Botões de Ajuste
                for botao in botoes_ajustes:
                    if botao['retangulo'].collidepoint(mouse_pos_clique):
                        acao = botao['acao']
                        
                        if acao == 'som':
                            config.SOM_LIGADO = not config.SOM_LIGADO
                            
                        elif acao in ["6x6", "8x8"]:
                            config.TAMANHO_TABULEIRO = acao
            
        
        # --- Lógica de Desenho ---
        tela.blit(img_fundo_ajustes, (0, 0))
        
        # Desenha os 3 Botões de Ajuste
        for botao in botoes_ajustes:
            rect = botao['retangulo']
            
            # 1. Verifica o estado de SELEÇÃO PERMANENTE 
            esta_selecionado = (botao['acao'] == 'som' and config.SOM_LIGADO) or \
                             (botao['acao'] in ["6x6", "8x8"] and config.TAMANHO_TABULEIRO == botao['acao'])
            
            
            # 2. Lógica de COR do Texto
            cor_texto = PRETO 
            
            if esta_selecionado:
                cor_texto = VERDE_DESTAQUE
                
            if rect.collidepoint(mouse_pos):
                cor_texto = VERDE_DESTAQUE 
                botao_atual_em_hover = rect # Rastreia o hover
                
            
            # 3. Desenha o texto do botão
            texto_render = fonte_botoes.render(botao['texto'], True, cor_texto)
            tela.blit(texto_render, texto_render.get_rect(center=rect.center))


        # --- Desenha o botão VOLTAR ---
        cor_texto_voltar = PRETO 
        
        # Lógica de HOVER para o botão VOLTAR
        if botao_voltar.collidepoint(mouse_pos):
            cor_texto_voltar = VERDE_DESTAQUE
            # Importante: Se o mouse estiver sobre este botão, ele substitui
            # qualquer hover dos botões de ajuste
            botao_atual_em_hover = botao_voltar 
            
        # Desenha o texto (com a cor de hover)
        texto_voltar = fonte_botoes.render("VOLTAR", True, cor_texto_voltar)
        tela.blit(texto_voltar, texto_voltar.get_rect(center=botao_voltar.center))
        
        # LÓGICA DO SOM DE HOVER (Centralizada e robusta)
        if SOM_BOTAO_HOVER is not None and config.SOM_LIGADO: # Adiciona a verificação do config.SOM_LIGADO
            # Se o mouse entrou em um novo botão
            if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                SOM_BOTAO_HOVER.play()

        # ATUALIZA o estado para o próximo loop
        # Esta linha agora é a única responsável por rastrear o estado.
        botao_em_hover_anterior = botao_atual_em_hover
        
        pygame.display.flip()

# --- Função Principal do Menu ---

def tela_de_menu(tela, largura_tela, altura_tela, fonte_titulo, fonte_botoes, img_fundo_menu, img_fundo_ajustes):
    """
    Exibe a tela de menu inicial, usa a imagem de fundo e gerencia a seleção de modo de jogo.
    """
    # NOVO BLOCO: Carrega o som aqui, garantindo que pygame.mixer.init() já foi chamado no main.py
    global SOM_BOTAO_HOVER # Indica que estamos usando a variável global
    if SOM_BOTAO_HOVER is None:
        try:
            SOM_BOTAO_HOVER = pygame.mixer.Sound('recursos/som_botao.wav')
        except pygame.error as e:
            print(f"Erro ao carregar som_botao.wav em tela_de_menu: {e}. O som de hover foi desativado.")
            SOM_BOTAO_HOVER = None

    botoes_config = get_botoes_config(largura_tela)
    
    # Rastreamento de hover para o som
    botao_em_hover_anterior = None 
    
    while True:
        mouse_pos = pygame.mouse.get_pos() 
        botao_atual_em_hover = None # Rastreador para este quadro
        
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
                            resultado_ajustes = tela_de_ajustes(
                                tela, largura_tela, altura_tela, 
                                fonte_titulo, fonte_botoes, 
                                img_fundo_menu, 
                                img_fundo_ajustes
                            )
                            if resultado_ajustes is None:
                                return None
                            
                        elif modo_escolhido == MODO_SAIR:
                            return None 
                            
                        elif modo_escolhido == MODO_PADRAO or modo_escolhido == MODO_MORTE_SUBITA or modo_escolhido == MODO_MELHOR_DE_3:
                            return modo_escolhido
                            
                        elif modo_escolhido == MODO_REGRAS:
                            resultado_regras = tela_de_regras(tela, largura_tela, altura_tela, fonte_botoes, PRETO, VERDE_DESTAQUE)
                            
                            if resultado_regras is None:
                                return None 
        
        # --- Lógica de Desenho ---
        
        # 1. Desenha o Fundo
        tela.blit(img_fundo_menu, (0, 0))
        
        # 2. Desenha os Botões e o Efeito Hover
        for botao in botoes_config:
            retangulo = botao['retangulo']
            texto = botao['texto']
            
            # 3.1. Define a Cor do Texto (Lógica de HOVER)
            if retangulo.collidepoint(mouse_pos):
                cor_texto = VERDE_DESTAQUE 
                botao_atual_em_hover = retangulo # Rastreia o hover aqui
            else:
                cor_texto = PRETO 
            
            # 3.2. Desenha o Texto, centralizado no retângulo invisível
            texto_renderizado = fonte_botoes.render(texto, True, cor_texto)
            tela.blit(texto_renderizado, texto_renderizado.get_rect(center=retangulo.center))
        
        # 4. LÓGICA DO SOM DE HOVER
        if SOM_BOTAO_HOVER is not None and config.SOM_LIGADO: # Adiciona a verificação do config.SOM_LIGADO
            # Se o mouse está sobre um botão AGORA, e NÃO ESTAVA sobre ele no quadro anterior
            if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                SOM_BOTAO_HOVER.play()

        # 5. ATUALIZA o estado para o próximo loop
        botao_em_hover_anterior = botao_atual_em_hover
        
        pygame.display.flip()