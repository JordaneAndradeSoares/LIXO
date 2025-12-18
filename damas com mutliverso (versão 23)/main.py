import pygame
import sys
import variaveis
import funcoes

# Inicializa a tela
tela = pygame.display.set_mode((variaveis.LARGURA, variaveis.ALTURA))
pygame.display.set_caption("Damas com Multiverso")

def main():
    funcoes.setup()
    clock = pygame.time.Clock()

    while True:
        funcoes.renderizar(tela)
        funcoes.centralizar_no_tabuleiro(variaveis.idx_ativa)  

        vitoria = funcoes.verificar_vitoria()
        empate = funcoes.verificar_empate()

        if empate:
            fonte = pygame.font.SysFont("Arial", 46, bold=True)
            txt = fonte.render("EMPATE NO MULTIVERSO!", True, variaveis.NEON_AMARELO)
            rect = txt.get_rect(center=(variaveis.LARGURA // 2, variaveis.ALTURA // 2))

            faixa = pygame.Surface((variaveis.LARGURA, 120))
            faixa.set_alpha(200)
            faixa.fill((0, 0, 0))
            tela.blit(faixa, (0, variaveis.ALTURA // 2 - 60))
            tela.blit(txt, rect)

            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            continue

        if  vitoria:
            # Se houver um vencedor, desenha o anúncio no centro da tela
            fonte_vitoria = pygame.font.SysFont("Arial", 50, bold=True)
            txt_surf = fonte_vitoria.render(vitoria, True, variaveis.NEON_BRANCO)
            txt_rect = txt_surf.get_rect(center=(variaveis.LARGURA // 2, variaveis.ALTURA // 2))
            
            # Desenha uma faixa preta atrás do texto para dar destaque
            faixa = pygame.Surface((variaveis.LARGURA, 120))
            faixa.set_alpha(200)
            faixa.fill((0, 0, 0))
            tela.blit(faixa, (0, variaveis.ALTURA // 2 - 60))
            tela.blit(txt_surf, txt_rect)
            
            # Atualiza o display para mostrar a vitória e pula o processamento de cliques
            pygame.display.flip()
            
            # Mantém o loop rodando apenas para permitir fechar o jogo
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            continue 

        # --- 1. LÓGICA DE SEGURAR (ESTADO CONTÍNUO) ---
        teclas = pygame.key.get_pressed()
        
        # Cálculo dinâmico do limite de rolagem do painel
        altura_total_conteudo = len(variaveis.timelines) * 45
        # O valor 200 compensa o cabeçalho e margens para a rolagem parar no lugar certo
        limite_maximo_painel = max(0, altura_total_conteudo - (variaveis.ALTURA - 200))

        # Se segurar a tecla, o movimento é suave (5 pixels por frame)
        if teclas[pygame.K_UP]:
            variaveis.rolagem_painel = max(0, variaveis.rolagem_painel - 5)
        if teclas[pygame.K_DOWN]:
            variaveis.rolagem_painel = min(limite_maximo_painel, variaveis.rolagem_painel + 5)

        # --- 2. PROCESSAMENTO DE EVENTOS ---
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            
            # CLIQUES DE TECLADO
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_t:
                    variaveis.modo_salto = not variaveis.modo_salto
                    variaveis.origem_salto_pos = None
                    variaveis.origem_salto_tl = None
                    variaveis.timeline_destino = None
                if ev.key == pygame.K_UP:
                    variaveis.rolagem_painel = max(0, variaveis.rolagem_painel - 40)
                if ev.key == pygame.K_DOWN:
                    variaveis.rolagem_painel = min(limite_maximo_painel, variaveis.rolagem_painel + 40)

            # CLIQUES DE MOUSE
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos
                
                # Clique no painel lateral (Seleção de Timeline)
                if mx > variaveis.LARGURA_AREA_TABULEIRO:
                    y_i = 150 - variaveis.rolagem_painel
                    for i in range(len(variaveis.timelines)):
                        # Verifica se o clique foi num item da lista
                        if y_i <= my <= y_i + 35:
                            if variaveis.modo_salto and variaveis.origem_salto_pos is not None:
                                # Apenas escolhe a timeline de destino
                                variaveis.timeline_destino = i

                                # Centraliza a timeline escolhida
                                variaveis.idx_ativa = i
                                variaveis.turno_visualizado = len(variaveis.timelines[i].historico) - 1
                                funcoes.centralizar_no_tabuleiro(i)
                                break

                            else: 
                                # Cancelar viagem no tempo ao trocar de timeline
                                variaveis.modo_salto = False
                                variaveis.origem_salto_pos = None
                                variaveis.origem_salto_tl = None

                                variaveis.idx_ativa = i
                                variaveis.turno_visualizado = len(variaveis.timelines[i].historico) - 1
                                funcoes.centralizar_no_tabuleiro(i)

                        y_i += 45
                
                # Clique na área dos tabuleiros
                else:
                    for i in range(len(variaveis.timelines)):
                        x_t = 100 + i * (variaveis.TABULEIRO_DIM + variaveis.ESPAÇAMENTO) - variaveis.rolagem_h
                        # Verifica se o clique foi dentro dos limites deste tabuleiro

                        if x_t <= mx <= x_t + variaveis.TABULEIRO_DIM and \
                            variaveis.TOPO_TABULEIRO <= my <= variaveis.TOPO_TABULEIRO + variaveis.TABULEIRO_DIM: 
                            coluna = (mx - x_t) // variaveis.CELULA
                            linha = (my - variaveis.TOPO_TABULEIRO) // variaveis.CELULA
                            funcoes.tratar_clique(i, int(linha), int(coluna))

        # Atualização da tela e controle de FPS
        pygame.display.flip()
        clock.tick(variaveis.FPS)

if __name__ == "__main__":
    main()