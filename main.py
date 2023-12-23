import pygame
import random
import time
from pygame.locals import *

pygame.init()

largura = 770
altura = 550

x = 40
y = 350

x_inimigo = 10
y_inimigo = 40

tamanho_1 = 90
tamanho_2 = 90
tamanho_3 = 100
tamanho_4 = 100

y_2 = y - tamanho_4
y_inimigo_2 = y_inimigo + tamanho_2

espacinho = x + 10
espacinho_texto = 10

fonte = pygame.font.SysFont("Arial", 10, True, True)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Wonder Weird World")

fps = pygame.time.Clock()

varivavel = 0

random.seed(int(time.time()))
numero_aleatorio = random.randint(1, 2)

while True:
    fps.tick(30)
    tela.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if numero_aleatorio == 1 and varivavel == 0:
        mensagem_de_entrada = "SEJA BEM VINDO! APERTE A TECLA A PARA JOGAR, VOCê COMEÇA DEFENDENCO"
        texto_de_entrada = fonte.render(mensagem_de_entrada, True, (255, 255, 255))
        tela.blit(texto_de_entrada, (x, altura / 2))
        
    if numero_aleatorio == 2 and varivavel == 0:
        mensagem_de_entrada = "SEJA BEM VINDO! APERTE A TECLA A PARA JOGAR, VOCÊ COMEÇA ATACANDO"
        texto_de_entrada = fonte.render(mensagem_de_entrada, True, (255, 255, 255))
        tela.blit(texto_de_entrada, (x, altura / 2))

    if pygame.key.get_pressed()[K_a] or varivavel != 0:
        varivavel = 1
        zona_aliada_1 = pygame.draw.rect(tela, (255, 0, 0), (x, y, tamanho_1, tamanho_2), 2)
        zona_aliada_2 = pygame.draw.rect(tela, (255, 0, 0), (x + tamanho_1, y, tamanho_1, tamanho_2), 2)
        zona_aliada_3 = pygame.draw.rect(tela, (255, 0, 0), (x + tamanho_1 * 2, y, tamanho_1, tamanho_2), 2)
        zona_aliada_4 = pygame.draw.rect(tela, (255, 0, 0), (x + tamanho_1 * 3, y, tamanho_1, tamanho_2), 2)
        zona_aliada_5 = pygame.draw.rect(tela, (255, 0, 0), (x + tamanho_1 * 4, y, tamanho_1, tamanho_2), 2)
        zona_aliada_6 = pygame.draw.rect(tela, (255, 0, 0), (x + tamanho_1 * 5, y, tamanho_1, tamanho_2), 2)

        zona_inimiga_1 = pygame.draw.rect(tela, (0, 255, 0), (x, y_inimigo, tamanho_1, tamanho_2), 2)
        zona_inimiga_2 = pygame.draw.rect(tela, (0, 255, 0), (x + tamanho_1, y_inimigo, tamanho_1, tamanho_2), 2)
        zona_inimiga_3 = pygame.draw.rect(tela, (0, 255, 0), (x + tamanho_1 * 2, y_inimigo, tamanho_1, tamanho_2), 2)
        zona_inimiga_4 = pygame.draw.rect(tela, (0, 255, 0), (x + tamanho_1 * 3, y_inimigo, tamanho_1, tamanho_2), 2)
        zona_inimiga_5 = pygame.draw.rect(tela, (0, 255, 0), (x + tamanho_1 * 4, y_inimigo, tamanho_1, tamanho_2), 2)
        zona_inimiga_6 = pygame.draw.rect(tela, (0, 255, 0), (x + tamanho_1 * 5, y_inimigo, tamanho_1, tamanho_2), 2)

        zona_aliada_de_batalha_1 = pygame.draw.rect(tela, (255, 0, 0), (x_inimigo, y_2, tamanho_3, tamanho_4), 2)
        zona_aliada_de_batalha_2 = pygame.draw.rect(tela, (255, 0, 0), (x_inimigo + tamanho_3, y_2, tamanho_3, tamanho_4), 2)
        zona_aliada_de_batalha_3 = pygame.draw.rect(tela, (255, 0, 0), (x_inimigo + tamanho_3 * 2, y_2, tamanho_3, tamanho_4), 2)
        zona_aliada_de_batalha_4 = pygame.draw.rect(tela, (255, 0, 0), (x_inimigo + tamanho_3 * 3, y_2, tamanho_3, tamanho_4), 2)
        zona_aliada_de_batalha_5 = pygame.draw.rect(tela, (255, 0, 0), (x_inimigo + tamanho_3 * 4, y_2, tamanho_3, tamanho_4), 2)
        zona_aliada_de_batalha_6 = pygame.draw.rect(tela, (255, 0, 0), (x_inimigo + tamanho_3 * 5, y_2, tamanho_3, tamanho_4), 2)

        zona_inimiga_de_batalha_1 = pygame.draw.rect(tela, (0, 255, 0), (x_inimigo, y_inimigo_2, tamanho_3, tamanho_4), 2)
        zona_inimiga_de_batalha_2 = pygame.draw.rect(tela, (0, 255, 0), (x_inimigo + tamanho_3, y_inimigo_2, tamanho_3, tamanho_4), 2)
        zona_inimiga_de_batalha_3 = pygame.draw.rect(tela, (0, 255, 0), (x_inimigo + tamanho_3 * 2, y_inimigo_2, tamanho_3, tamanho_4), 2)
        zona_inimiga_de_batalha_4 = pygame.draw.rect(tela, (0, 255, 0), (x_inimigo + tamanho_3 * 3, y_inimigo_2, tamanho_3, tamanho_4), 2)
        zona_inimiga_de_batalha_5 = pygame.draw.rect(tela, (0, 255, 0), (x_inimigo + tamanho_3 * 4, y_inimigo_2, tamanho_3, tamanho_4), 2)
        zona_inimiga_de_batalha_6 = pygame.draw.rect(tela, (0, 255, 0), (x_inimigo + tamanho_3 * 5, y_inimigo_2, tamanho_3, tamanho_4), 2)

        mensagem_cemiterio = "CEMITERIO"
        mensagem_deck = "DECK"

        texto_aliado_cemiterio = fonte.render(mensagem_cemiterio, True, (255, 255, 255))
        texto_aliado_deck = fonte.render(mensagem_deck, True, (255, 255, 255))
        texto_inimigo_cemiterio = fonte.render(mensagem_cemiterio, True, (255, 255, 255))
        texto_inimigo_deck = fonte.render(mensagem_deck, True, (255, 255, 255))

        tela.blit(texto_aliado_cemiterio, (x + espacinho + espacinho_texto + tamanho_1 * 6, espacinho_texto + y - tamanho_2))
        tela.blit(texto_aliado_deck, (x + espacinho + espacinho_texto + tamanho_1 * 6, espacinho_texto + y))
        tela.blit(texto_inimigo_cemiterio, (x + espacinho + espacinho_texto + tamanho_1 * 6, espacinho_texto + y_inimigo))
        tela.blit(texto_inimigo_deck, (x + espacinho + espacinho_texto + tamanho_1 * 6, espacinho_texto + y_inimigo + tamanho_2))

        cemiterio_aliado = pygame.draw.rect(tela, (255, 0, 0), (x + espacinho + tamanho_1 * 6, y - tamanho_2, tamanho_1, tamanho_2), 2)
        cemiterio_inimigo = pygame.draw.rect(tela, (0, 255, 0), (x + espacinho + tamanho_1 * 6, y_inimigo, tamanho_1, tamanho_2), 2)

        deck_aliado = pygame.draw.rect(tela, (255, 0, 0), (x + espacinho + tamanho_1 * 6, y, tamanho_1, tamanho_2), 2)
        deck_inimigo = pygame.draw.rect(tela, (0, 255, 0), (x + espacinho + tamanho_1 * 6, y_inimigo + tamanho_2, tamanho_1, tamanho_2), 2)

    pygame.display.update()
