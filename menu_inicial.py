import pygame
import cores # Se 'cores' for um módulo separado, como no seu código

# --- Novos Modos de Jogo ---
MODO_PADRAO = 'padrao'
MODO_MELHOR_DE_3 = 'melhor_de_3'
MODO_MORTE_SUBITA = 'morte_subita'

# --- Novas Cores ---
cores.verde_claro = (144, 238, 144)
cores.vermelho_claro = (255, 182, 193)

def tela_de_menu(tela, largura_tela, altura_tela, fonte_titulo, fonte_botoes):
    """
    Exibe a tela de menu inicial e gerencia a seleção de modo de jogo.
    Retorna o modo de jogo escolhido.
    """
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                
                # Coordenadas dos botões
                # Você pode calcular as coordenadas de forma dinâmica para telas de tamanhos diferentes.
                # Aqui estão valores fixos para simplificar o exemplo.
                botao_padrao = pygame.Rect(largura_tela // 2 - 100, 150, 200, 50)
                botao_melhor_de_3 = pygame.Rect(largura_tela // 2 - 100, 250, 200, 50)
                botao_morte_subita = pygame.Rect(largura_tela // 2 - 100, 350, 200, 50)

                # Verifica qual botão foi clicado
                if botao_padrao.collidepoint((mouse_x, mouse_y)):
                    return MODO_PADRAO
                if botao_melhor_de_3.collidepoint((mouse_x, mouse_y)):
                    return MODO_MELHOR_DE_3
                if botao_morte_subita.collidepoint((mouse_x, mouse_y)):
                    return MODO_MORTE_SUBITA
        
        # Desenha o fundo
        tela.fill(cores.azul_claro)
        
        # Desenha o título
        titulo_txt = fonte_titulo.render("Caça ao Tesouro", True, cores.preto)
        tela.blit(titulo_txt, titulo_txt.get_rect(center=(largura_tela // 2, 50)))
        
        # Desenha os botões
        botao_padrao = pygame.Rect(largura_tela // 2 - 100, 150, 200, 50)
        pygame.draw.rect(tela, cores.branco, botao_padrao)
        texto_padrao = fonte_botoes.render("Padrão", True, cores.preto)
        tela.blit(texto_padrao, texto_padrao.get_rect(center=botao_padrao.center))

        botao_melhor_de_3 = pygame.Rect(largura_tela // 2 - 100, 250, 200, 50)
        pygame.draw.rect(tela, cores.branco, botao_melhor_de_3)
        texto_melhor_de_3 = fonte_botoes.render("Melhor de 3", True, cores.preto)
        tela.blit(texto_melhor_de_3, texto_melhor_de_3.get_rect(center=botao_melhor_de_3.center))

        botao_morte_subita = pygame.Rect(largura_tela // 2 - 100, 350, 200, 50)
        pygame.draw.rect(tela, cores.branco, botao_morte_subita)
        texto_morte_subita = fonte_botoes.render("Morte Súbita", True, cores.preto)
        tela.blit(texto_morte_subita, texto_morte_subita.get_rect(center=botao_morte_subita.center))
        
        pygame.display.flip()