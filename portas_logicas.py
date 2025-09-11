import pygame
import sys

pygame.init()

# Cores
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
BRANCO = (255, 255, 255)
CINZA = (180, 180, 180)

# Tela e fonte
LARGURA, ALTURA = 800, 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
fonte = pygame.font.SysFont("Arial", 26, True, True)

pygame.display.set_caption("Portas Lógicas: Vemelho = 1 e Cinza = 0")

# Estados dos botões
A = False  # Entrada A
B = False  # Entrada B
inv_A = False  # Inversor de A
inv_B = False  # Inversor de B

# Retângulos dos botões
botao_verde = pygame.Rect(150, 300, 50, 50)
botao_azul = pygame.Rect(600, 300, 50, 50)
botao_saida = pygame.Rect(350, 100, 50, 50)

botao_inv_A = pygame.Rect(220, 300, 30, 30)
botao_inv_B = pygame.Rect(670, 300, 30, 30)

# Porta lógica selecionada
modo = "AND"  # pode ser: AND, NAND, OR, NOR, XOR, NXOR

def calcular_saida(A, B, inv_A, inv_B, modo):
    # aplicar inversores
    if inv_A:
        A = not A
    if inv_B:
        B = not B

    if modo == "AND":
        return A and B
    elif modo == "NAND":
        return not (A and B)
    elif modo == "OR":
        return A or B
    elif modo == "NOR":
        return not (A or B)
    elif modo == "XOR":
        return A ^ B
    elif modo == "NXOR":
        return not (A ^ B)
    return False

while True:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if botao_verde.collidepoint(evento.pos):
                A = not A
            elif botao_azul.collidepoint(evento.pos):
                B = not B
            elif botao_inv_A.collidepoint(evento.pos):
                inv_A = not inv_A
            elif botao_inv_B.collidepoint(evento.pos):
                inv_B = not inv_B
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                modo = "AND"
            elif evento.key == pygame.K_2:
                modo = "NAND"
            elif evento.key == pygame.K_3:
                modo = "OR"
            elif evento.key == pygame.K_4:
                modo = "NOR"
            elif evento.key == pygame.K_5:
                modo = "XOR"
            elif evento.key == pygame.K_6:
                modo = "NXOR"

    # Calcular saída
    porta = calcular_saida(A, B, inv_A, inv_B, modo)

    # Mostrar saída (botão vermelho acende ou apaga)
    pygame.draw.rect(tela, VERMELHO if porta else CINZA, botao_saida)

    # Entrada A (verde)
    pygame.draw.rect(tela, VERDE, botao_verde)
    if A:
        pygame.draw.rect(tela, PRETO, botao_verde, 3)

    # Inversor de A
    pygame.draw.rect(tela, CINZA, botao_inv_A)
    if inv_A:
        pygame.draw.rect(tela, PRETO, botao_inv_A, 3)

    # Entrada B (azul)
    pygame.draw.rect(tela, AZUL, botao_azul)
    if B:
        pygame.draw.rect(tela, PRETO, botao_azul, 3)

    # Inversor de B
    pygame.draw.rect(tela, CINZA, botao_inv_B)
    if inv_B:
        pygame.draw.rect(tela, PRETO, botao_inv_B, 3)

    # Mostrar nome da porta lógica
    texto = fonte.render(f"Porta: {modo}", True, PRETO)
    tela.blit(texto, (320, 50))

    instrucoes = fonte.render("1=AND  2=NAND  3=OR  4=NOR  5=XOR  6=NXOR", True, PRETO)
    tela.blit(instrucoes, (100, 360))

    inv_texto = fonte.render("Inv A", True, PRETO)
    tela.blit(inv_texto, (215, 270))
    inv_texto = fonte.render("Inv B", True, PRETO)
    tela.blit(inv_texto, (665, 270))

    pygame.display.update()