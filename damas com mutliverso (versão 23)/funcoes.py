import pygame
import copy
import variaveis
from classes import GestorID, LinhaDoTempo, MotorRegras, GestorTimelineID

def setup():
    tab = [[None for _ in range(8)] for _ in range(8)]
    for r in range(3):
        for c in range(8):
            if (r + c) % 2 == 1: tab[r][c] = ('b', GestorID.gerar())

    for r in range(5, 8):
        for c in range(8):
            if (r + c) % 2 == 1: tab[r][c] = ('r', GestorID.gerar())
            
    variaveis.timelines.append(LinhaDoTempo("1", tab, 'r'))

def renderizar(tela):
    tela.fill(variaveis.FUNDO)
    
    # --- 1. DESENHO DOS TABULEIROS ---
    for i, tl in enumerate(variaveis.timelines):
        x = 100 + i * (variaveis.TABULEIRO_DIM + variaveis.ESPAÇAMENTO) - variaveis.rolagem_h
        
        if x + variaveis.TABULEIRO_DIM < 0 or x > variaveis.LARGURA_AREA_TABULEIRO: 
            continue
        
        cor_frame = variaveis.NEON_AMARELO if i == variaveis.idx_ativa else (40, 45, 60)
        if variaveis.modo_salto and i == variaveis.origem_salto_tl: 
            cor_frame = variaveis.NEON_ROXO
            
        pygame.draw.rect(tela, cor_frame, (x-6, variaveis.TOPO_TABULEIRO-6, variaveis.TABULEIRO_DIM+12, variaveis.TABULEIRO_DIM+12), 4, border_radius=10)
        
        indice_seguro = min(variaveis.turno_visualizado, len(tl.historico) - 1)
        tab_visual = tl.historico[indice_seguro] if i == variaveis.idx_ativa else tl.estado_atual

        for r in range(8):
            for c in range(8):
                cx = x + c * variaveis.CELULA
                cy = variaveis.TOPO_TABULEIRO + r * variaveis.CELULA
                rect_casa = (cx, cy, variaveis.CELULA, variaveis.CELULA)
                
                cor_casa = variaveis.TAB_ESCURO if (r + c) % 2 == 1 else variaveis.TAB_CLARO
                pygame.draw.rect(tela, cor_casa, rect_casa)
                
                if i == variaveis.idx_ativa and variaveis.peca_sel:
                    motor = MotorRegras(tl.estado_atual)
                    validos = motor.obter_validos(tl.cor_vez)
                    if variaveis.peca_sel in validos:
                        for dest in validos[variaveis.peca_sel]:
                            if r == dest[0] and c == dest[1]:
                                pygame.draw.circle(tela, (0, 255, 255), (cx + 30, cy + 30), 10)

                if variaveis.modo_salto and variaveis.origem_salto_pos:
                    if i != variaveis.origem_salto_tl and tab_visual[r][c] is None and (r + c) % 2 == 1:
                        pygame.draw.rect(tela, variaveis.NEON_ROXO, rect_casa, 2)

                peca = tab_visual[r][c]
                if peca:
                    cor_p = variaveis.NEON_VERMELHO if peca[0].lower() == 'r' else variaveis.NEON_VERDE
                    px, py = cx + 30, cy + 30

                    if variaveis.modo_salto and i == variaveis.origem_salto_tl and variaveis.origem_salto_pos == (r, c):
                        pygame.draw.circle(tela, variaveis.NEON_ROXO, (px, py), 28, 3)

                    # Desenho Base da Peça
                    pygame.draw.circle(tela, cor_p, (px, py), 22)

                    # --- VISUAL DA PROMOÇÃO (DAMA) ---
                    # Se a letra for maiúscula, adiciona um aro dourado e um centro brilhante
                    if peca[0].isupper(): 
                        pygame.draw.circle(tela, (255, 215, 0), (px, py), 25, 4) # Aro Dourado
                        pygame.draw.circle(tela, (255, 255, 255), (px, py), 8)  # Brilho Central
                    
                    id_txt = variaveis.F_NOME.render(str(peca[1]), True, (0, 0, 0))
                    tela.blit(id_txt, id_txt.get_rect(center=(px, py)))
        
        lbl_id = variaveis.F_NOME.render(f"REALIDADE {tl.nome}", True, variaveis.NEON_BRANCO)
        tela.blit(lbl_id, (x, variaveis.TOPO_TABULEIRO + variaveis.TABULEIRO_DIM + 15))
        
        cor_vez_txt = variaveis.NEON_VERMELHO if tl.cor_vez == 'r' else variaveis.NEON_VERDE
        lbl_vez = variaveis.F_UI.render(f"VEZ: {'VERMELHO' if tl.cor_vez == 'r' else 'VERDE'}", True, cor_vez_txt)
        tela.blit(lbl_vez, (x, variaveis.TOPO_TABULEIRO + variaveis.TABULEIRO_DIM + 35))

    # --- PAINEL LATERAL ---
    pygame.draw.rect(tela, (15, 18, 25), (variaveis.LARGURA_AREA_TABULEIRO, 0, variaveis.LARGURA_PAINEL_UI, variaveis.ALTURA))
    tela.blit(variaveis.F_TITULO.render("MULTIVERSO", True, variaveis.NEON_AZUL), (variaveis.LARGURA_AREA_TABULEIRO + 20, 50))
    
    aviso_cor = variaveis.NEON_ROXO if variaveis.modo_salto else variaveis.TEXTO_FOSCO
    comando = " (altere de modo usando a tecla T)"
    txt_modo = "VIAGEM ATIVA - escolha a peça, timeline e casa" + comando if variaveis.modo_salto else "MODO NORMAL" + comando
    tela.blit(variaveis.F_AVISO.render(txt_modo, True, aviso_cor), (10, 10))

    y_l = 150 - variaveis.rolagem_painel 
    for i, tl in enumerate(variaveis.timelines):
        if 130 <= y_l <= variaveis.ALTURA - 30:
            cor_item = variaveis.NEON_AMARELO if i == variaveis.idx_ativa else variaveis.TEXTO_FOSCO
            cor_bola = variaveis.NEON_VERMELHO if tl.cor_vez == 'r' else variaveis.NEON_VERDE
            pygame.draw.circle(tela, cor_bola, (variaveis.LARGURA_AREA_TABULEIRO + 25, y_l + 12), 6)
            tela.blit(variaveis.F_UI.render(f"Realidade {tl.nome}", True, cor_item), (variaveis.LARGURA_AREA_TABULEIRO + 45, y_l))
        y_l += 45

def verificar_vitoria():
    """
    Nova Lógica: Se qualquer timeline for limpa de uma cor, 
    o jogo termina naquela realidade afetando o multiverso.
    """
    for tl in variaveis.timelines:
        tem_r = False
        tem_b = False
        for linha in tl.estado_atual:
            for peca in linha:
                if peca:
                    if peca[0].lower() == 'r': tem_r = True
                    if peca[0].lower() == 'b': tem_b = True
        
        # Se nesta timeline específica alguém foi exterminado:
        if not tem_r: return "VERDES VENCERAM O MULTIVERSO!"
        if not tem_b: return "VERMELHOS VENCERAM O MULTIVERSO!"
    return None

def verificar_empate():
    for tl in variaveis.timelines:
        ocupadas = 0
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 != 0 and tl.estado_atual[r][c] is not None:
                    ocupadas += 1
        
        # Existem 32 casas pretas num tabuleiro 8x8
        if ocupadas == 32:
            return True
    return False

def obter_linhagem_descendente(nome_pai):
    descendentes = [nome_pai]
    for tl in variaveis.timelines:
        if tl.nome.startswith(nome_pai + "."): descendentes.append(tl.nome)
    return descendentes

def criar_ramificacao(or_idx, or_r, or_c, dest_idx, dest_r, dest_c):
    tl_origem = variaveis.timelines[or_idx]
    tl_destino = variaveis.timelines[dest_idx]
    
    # 1. Identifica a peça que será clonada
    peca_original = tl_origem.estado_atual[or_r][or_c]

    if not peca_original: 
        return

    # 2. Define nome da nova realidade
    tl_origem.proximo_filho += 1
    novo_nome = f"{tl_origem.nome}.{tl_origem.proximo_filho}" if tl_origem.nome != "1" else str(tl_origem.proximo_filho + 1)

    # 3. Cria o novo tabuleiro duplicando a peça no destino
    novo_tabuleiro = copy.deepcopy(tl_destino.estado_atual)
    novo_tabuleiro[dest_r][dest_c] = peca_original

    # 4. Adiciona a nova realidade à lista global
    cor_proxima = 'b' if peca_original[0].lower() == 'r' else 'r'
    nova_tl = LinhaDoTempo(novo_nome, novo_tabuleiro, cor_proxima)
    variaveis.timelines.append(nova_tl)

    # 5. Reset UI e Foco
    variaveis.modo_salto = False
    variaveis.origem_salto_pos = None
    variaveis.origem_salto_tl = None
    variaveis.idx_ativa = len(variaveis.timelines) - 1
    variaveis.turno_visualizado = 0
    centralizar_no_tabuleiro(variaveis.idx_ativa)  

    # Se Vermelho ('r') chega na linha 0 ou Verde ('b') chega na linha 7
    if (peca_original[0].lower() == 'r' and dest_r == 0) or (peca_original[0].lower() == 'b' and dest_r == 7):
        promover_peca(peca_original[1]) # Isso força a atualização em todas as timelines
    
def tratar_clique(idx_tl, r, c):
    tl = variaveis.timelines[idx_tl]
    
    if variaveis.modo_salto:

        # ETAPA 1 — escolher peça
        if variaveis.origem_salto_pos is None:
            if tl.estado_atual[r][c] and tl.estado_atual[r][c][0].lower() == tl.cor_vez:
                variaveis.origem_salto_tl = idx_tl
                variaveis.origem_salto_pos = (r, c)

                centralizar_no_tabuleiro(idx_tl)
            return

        # ETAPA 2 — timeline ainda não escolhida
        if variaveis.timeline_destino is None:
            return  # ignora cliques no tabuleiro

        # ETAPA 3 — escolher casa preta livre
        if idx_tl == variaveis.timeline_destino:
            if tl.estado_atual[r][c] is None and (r + c) % 2 == 1:
                criar_ramificacao(
                    variaveis.origem_salto_tl,
                    variaveis.origem_salto_pos[0],
                    variaveis.origem_salto_pos[1],
                    idx_tl, r, c
                )

                # Reset total da viagem
                variaveis.modo_salto = False
                variaveis.origem_salto_pos = None
                variaveis.origem_salto_tl = None
                variaveis.timeline_destino = None
            return

    # Se não estiver no modo salto, processa a movimentação normal
    if idx_tl != variaveis.idx_ativa: return
    tab_foco = tl.estado_atual
    
    if tab_foco[r][c] and tab_foco[r][c][0].lower() == tl.cor_vez:
        variaveis.peca_sel = (r, c)
    elif variaveis.peca_sel:
        or_r, or_c = variaveis.peca_sel
        motor = MotorRegras(tab_foco)
        validos = motor.obter_validos(tl.cor_vez)
        
        if (or_r, or_c) in validos and (r, c) in validos[(or_r, or_c)]:
            peca_movida = tab_foco[or_r][or_c]
            
            # Lógica de Captura
            if abs(r - or_r) == 2:
                v_r, v_c = (r + or_r) // 2, (c + or_c) // 2
                vitima = tab_foco[v_r][v_c]
                if vitima: 
                    apagar_peca(vitima[1])  # Remove a peça capturada e seus descendentes
                    tab_foco[v_r][v_c] = None
            
            # Executa o Movimento no tabuleiro atual
            tab_foco[r][c] = peca_movida
            tab_foco[or_r][or_c] = None
            
            # --- PROMOÇÃO IMEDIATA ---
            # Verifica promoção ANTES de salvar o histórico para que a imagem já apareça como Dama
            if (peca_movida[0].lower() == 'r' and r == 0) or (peca_movida[0].lower() == 'b' and r == 7):
                promover_peca(peca_movida[1]) 
            
            # Atualiza Histórico e Interface
            tl.historico.append(copy.deepcopy(tab_foco))
            tl.cor_vez = 'b' if tl.cor_vez == 'r' else 'r'
            variaveis.turno_visualizado = len(tl.historico) - 1
            variaveis.peca_sel = None

    # Sempre centraliza a timeline clicada
    centralizar_no_tabuleiro(idx_tl)
        
def centralizar_no_tabuleiro(idx_tl):
    pos_x = 100 + idx_tl * (variaveis.TABULEIRO_DIM + variaveis.ESPAÇAMENTO)
    centro = variaveis.LARGURA_AREA_TABULEIRO // 2
    variaveis.rolagem_h = pos_x - centro + (variaveis.TABULEIRO_DIM // 2)

def apagar_peca(peca_id):
    for tl in variaveis.timelines:
        mudou = False
        for r in range(8):
            for c in range(8):
                p = tl.estado_atual[r][c]
                if p and p[1] == peca_id:
                    tl.estado_atual[r][c] = None
                    mudou = True
        if mudou:
            tl.historico.append(copy.deepcopy(tl.estado_atual))

def promover_peca(peca_id):
    for idx, tl in enumerate(variaveis.timelines):
        mudou = False
        for r in range(8):
            for c in range(8):
                p = tl.estado_atual[r][c]
                if p and p[1] == peca_id and not p[0].isupper():
                    tl.estado_atual[r][c] = (p[0].upper(), p[1])
                    mudou = True

        if mudou:
            tl.historico.append(copy.deepcopy(tl.estado_atual))

            # FORÇA ATUALIZAÇÃO VISUAL SE FOR A TIMELINE ATIVA
            if idx == variaveis.idx_ativa:
                variaveis.turno_visualizado = len(tl.historico) - 1
