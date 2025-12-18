import pygame
pygame.init()
pygame.font.init()

# Inicialização de fontes para evitar erros nos outros arquivos
pygame.font.init()

FPS = 60
LARGURA, ALTURA = 1450, 750
LARGURA_PAINEL_UI = 480
LARGURA_AREA_TABULEIRO = LARGURA - LARGURA_PAINEL_UI

CELULA = 60
TABULEIRO_DIM = CELULA * 8
ESPAÇAMENTO = 75
TOPO_TABULEIRO = 130

# Cores
FUNDO = (8, 10, 15)
TAB_ESCURO = (18, 22, 32)
TAB_CLARO = (215, 220, 230)
NEON_AZUL = (0, 191, 255)
NEON_VERDE = (50, 255, 126)
NEON_VERMELHO = (255, 56, 82)
NEON_AMARELO = (255, 211, 42)
NEON_ROXO = (160, 32, 240)
NEON_BRANCO = (240, 245, 255)
TEXTO_FOSCO = (110, 120, 140)

# Variáveis Globais de Estado
timelines = []

idx_ativa = 0
turno_visualizado = 0 
rolagem_painel = 0
rolagem_h = 0

# Variáveis para controlar a viagem no tempo
modo_salto = False  # Usado para alternar entre modos
origem_salto_pos = None  # Para armazenar a posição original antes de viajar
alvo_salto_tl = None  # Para armazenar a timeline alvo da viagem

peca_sel = None
origem_salto_tl = None
origem_salto_pos = None  
alvo_salto_tl = None
timeline_destino = None

# Fontes
try:
    F_TITULO = pygame.font.SysFont("Segoe UI", 34, bold=True)
    F_UI = pygame.font.SysFont("Segoe UI", 18, bold=True)
    F_NOME = pygame.font.SysFont("Consolas", 15, bold=True)
    F_AVISO = pygame.font.SysFont("Segoe UI", 22, bold=True)
except:
    F_TITULO = pygame.font.SysFont("Arial", 34, bold=True)
    F_UI = pygame.font.SysFont("Arial", 18, bold=True)
    F_NOME = pygame.font.SysFont("Arial", 15, bold=True)
    F_AVISO = pygame.font.SysFont("Arial", 22, bold=True)