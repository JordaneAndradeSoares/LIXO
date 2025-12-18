import pygame
import copy

class GestorTimelineID:
    _contador = 0

    @classmethod
    def gerar(cls):
        cls._contador += 1
        return str(cls._contador)

class GestorID:
    _contador = 0
    @classmethod
    def gerar(cls):
        cls._contador += 1
        return str(cls._contador)

class LinhaDoTempo:
    def __init__(self, nome, estado_inicial, cor_vez):
        self.nome = nome
        self.estado_atual = estado_inicial
        self.historico = [copy.deepcopy(estado_inicial)]
        self.cor_vez = cor_vez
        self.proximo_filho = 0

class MotorRegras:
    def __init__(self, tabuleiro):
        self.tabuleiro = tabuleiro

    def obter_validos(self, cor):
        tem_captura = False
        dict_caps, dict_movs = {}, {}
        for r in range(8):
            for c in range(8):
                p = self.tabuleiro[r][c]
                if p and p[0].lower() == cor:
                    movs, caps = self.calcular_peca(r, c)
                    if caps:
                        dict_caps[(r, c)] = caps
                        tem_captura = True
                    if movs:
                        dict_movs[(r, c)] = movs
        return dict_caps if tem_captura else dict_movs

    def calcular_peca(self, r, c):
        p = self.tabuleiro[r][c]
        tipo = p[0]
        movs, caps = [], []
        # Direções: Damas (todas) ou Peões (conforme a cor)
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if tipo.isupper() else \
               ([(-1, -1), (-1, 1)] if tipo == 'r' else [(1, -1), (1, 1)])
        
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.tabuleiro[nr][nc] is None:
                    movs.append((nr, nc))
                elif self.tabuleiro[nr][nc][0].lower() != tipo.lower():
                    sr, sc = nr + dr, nc + dc
                    if 0 <= sr < 8 and 0 <= sc < 8 and self.tabuleiro[sr][sc] is None:
                        caps.append((sr, sc))
        return movs, caps