import pygame
from pygame.locals import * 
from sys import exit
from random import randint

pygame.init()

largura = 640
altura = 480

x = largura / 2
y = altura / 2

x_2 = largura / 2 + 60
y_2 = altura / 2 

movimento = 20

pontos = 0
fonte = pygame.font.SysFont("Arial", 40, True, True)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("JOGO DE CARTAS")

fps = pygame.time.Clock()

while True:
    fps.tick(30)

    tela.fill((0,0,0))

    mensagem  = f"Pontos: {pontos}"
    texto = fonte.render(mensagem, True, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if pygame.key.get_pressed()[K_a]:
        x = x - movimento
    if pygame.key.get_pressed()[K_d]:
        x = x + movimento
    if pygame.key.get_pressed()[K_w]:
        y = y - movimento
    if pygame.key.get_pressed()[K_s]:
        y = y + movimento

    if x > largura:
        x = 0
    if x < 0:
        x = largura
    if y < 0:
        y = altura
    if y > altura:
        y = 0

    jogador = pygame.draw.rect(tela, (255, 0, 0), (x, y, 40, 69))
    outro_retangulo = pygame.draw.rect(tela, (0, 255, 0), (x_2, y_2, 40, 69))

    if jogador.colliderect(outro_retangulo):
        x_2 = randint(40, 600)
        y_2 = randint(50, 430)

        pontos += 1

    tela.blit(texto, (400, 40))
    
    pygame.display.update()