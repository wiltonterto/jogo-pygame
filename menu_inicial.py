import pygame
import cores 
import config

# --- Constantes de Modos de Jogo ---
MODO_PADRAO = 'padrao'
MODO_MELHOR_DE_3 = 'melhor_de_3'
MODO_MORTE_SUBITA = 'morte_subita'
MODO_AJUSTES = 'ajustes'   # NOVO: Para a tela 4.png
MODO_REGRAS = 'regras'     # NOVO
MODO_SAIR = 'sair'         # NOVO

# --- Constantes de Cores para o Hover ---

PRETO = (0, 0, 0) 
# Use uma cor de destaque para o hover (você pode ajustar este verde)
VERDE_DESTAQUE = (144, 238, 144) 
# Cor para o título (o tom dourado da sua imagem, ou preto se preferir)
COR_TITULO = (30, 30, 30) 

# --- Constantes Visuais para AJUSTES (Baseado no design 4.png) ---
LARGURA_QUADRADO = 180
ALTURA_QUADRADO = 180
ESPACO_QUADRADO = 200 # Distância entre os centros dos quadrados
Y_BOTOES_AJUSTES = 350 # Altura dos 3 botões quadrados

# Cores para o toggle
COR_BOTAO_LIGADO = (144, 238, 144) # O verde do seu hover
COR_BOTAO_DESLIGADO = (220, 220, 220) # Um cinza claro

# --- Funções de Configuração ---

def get_botoes_config(largura_tela):
    """Define as posições e ações de todos os botões do menu."""
    
    LARGURA_BOTAO = 240 # Largura visual aproximada da pílula
    ALTURA_BOTAO = 50   # Altura visual aproximada da pílula
    ESPACO_VERTICAL = 70 # Distância entre os centros dos botões
    
    # O ponto X onde o retângulo de clique começa (centralizado em 1050px)
    x_start = largura_tela // 2 - LARGURA_BOTAO // 2 
    
    # O ponto Y onde o primeiro botão (Modo Padrão) está centralizado na imagem
    y_start_base = 395
    
    return [
        {'texto': "MODO PADRÃO", 'modo': MODO_PADRAO, 
         'retangulo': pygame.Rect(x_start, y_start_base, LARGURA_BOTAO, ALTURA_BOTAO)},
        
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
    
    # Botão Voltar (na parte inferior)
    botao_voltar = pygame.Rect(x_center - 100, altura_tela - 150, 200, 50)
    
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
        # ATENÇÃO: Usa a imagem de fundo de AJUSTES!
        tela.blit(img_fundo_ajustes, (0, 0))
        
        # Desenha os 3 Botões de Ajuste
        for botao in botoes_ajustes:
            rect = botao['retangulo']
            
            # Escolhe a cor de destaque (Toggle e Seleção)
            cor_destaque = COR_BOTAO_DESLIGADO
            if botao['acao'] == 'som' and config.SOM_LIGADO:
                cor_destaque = COR_BOTAO_LIGADO
            elif botao['acao'] in ["6x6", "8x8"] and config.TAMANHO_TABULEIRO == botao['acao']:
                cor_destaque = COR_BOTAO_LIGADO
                
            # Efeito Hover: Contorno Verde
            contorno = 0
            if rect.collidepoint(mouse_pos):
                contorno = 3 
                
            pygame.draw.rect(tela, cor_destaque, rect, border_radius=15)
            pygame.draw.rect(tela, VERDE_DESTAQUE, rect, contorno, border_radius=15)
            
            # Desenha o texto do botão
            texto_render = fonte_botoes.render(botao['texto'], True, PRETO)
            tela.blit(texto_render, texto_render.get_rect(center=rect.center))


        # Desenha o botão VOLTAR
        cor_voltar = COR_BOTAO_DESLIGADO
        contorno_voltar = 0
        if botao_voltar.collidepoint(mouse_pos):
            contorno_voltar = 3
            
        pygame.draw.rect(tela, cor_voltar, botao_voltar, border_radius=15)
        pygame.draw.rect(tela, VERDE_DESTAQUE, botao_voltar, contorno_voltar, border_radius=15)
        
        texto_voltar = fonte_botoes.render("VOLTAR", True, PRETO)
        tela.blit(texto_voltar, texto_voltar.get_rect(center=botao_voltar.center))
        
        pygame.display.flip()


# --- Função Principal do Menu ---

# A FUNÇÃO AGORA RECEBE AS DUAS IMAGENS DE FUNDO!
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
                            # SE CLICAR EM AJUSTES, CHAMA A NOVA TELA E REPASSA AS DUAS IMAGENS
                            resultado_ajustes = tela_de_ajustes(
                                tela, largura_tela, altura_tela, 
                                fonte_titulo, fonte_botoes, 
                                img_fundo_menu,             
                                img_fundo_ajustes           # <--- Repasse correto!
                            )
                            if resultado_ajustes is None:
                                return None
                            
                        else:
                            return modo_escolhido
        
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