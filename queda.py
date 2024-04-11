import pygame
import sys
from random import randint

pygame.init()

LARGURA = 300
ALTURA = 400

x_jogador = LARGURA // 2
y_jogador = ALTURA // 2

tamanho = 10
largura_obstaculo = LARGURA - (tamanho * 4)

y_parede = ALTURA + tamanho
x_parede = randint(0, LARGURA - largura_obstaculo)

jogo_ativo = False
derrota = False

velocidade_de_deslocamento = 10
velocidade_de_queda = 2
 
clock = pygame.time.Clock()
fonte = pygame.font.SysFont('arial', 8, True, True)
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Queda")

teclas_press = {pygame.K_a: False, pygame.K_d: False}

while True:
    janela.fill((0, 0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if not jogo_ativo and evento.key == pygame.K_k:
                jogo_ativo = True
            if evento.key in teclas_press:
                teclas_press[evento.key] = True

        if evento.type == pygame.KEYUP:
            if evento.key in teclas_press:
                teclas_press[evento.key] = False

    if jogo_ativo:

        jogador = pygame.Rect(x_jogador, y_jogador, tamanho, tamanho)
        parede_subindo = pygame.Rect(x_parede, y_parede, largura_obstaculo, tamanho)

        if y_parede < -tamanho:
            x_parede = randint(0, LARGURA - largura_obstaculo)
            y_parede = ALTURA + tamanho

        if y_jogador > ALTURA + tamanho:
            y_jogador = -tamanho

        if jogador.colliderect(parede_subindo):
            y_jogador = y_parede - tamanho
                
            if y_jogador <= -tamanho:
                derrota = True
                jogo_ativo = False

        if teclas_press[pygame.K_a] and x_jogador > 0:
            x_jogador -= velocidade_de_deslocamento
        if teclas_press[pygame.K_d] and x_jogador < LARGURA - tamanho:
            x_jogador += velocidade_de_deslocamento

        pygame.draw.rect(janela, (255, 0, 0), (x_jogador, y_jogador, tamanho, tamanho))
        pygame.draw.rect(janela, (255, 255, 255), (x_parede, y_parede, largura_obstaculo, tamanho))

        y_parede -= velocidade_de_queda
        y_jogador += velocidade_de_queda

    if not jogo_ativo:
        y_parede = ALTURA + tamanho
        x_jogador = LARGURA // 2
        y_jogador = ALTURA // 2

        if derrota:
            texto_2 = fonte.render("Derrota!", True, (255, 0, 0))
            janela.blit(texto_2, (LARGURA // 10 , ALTURA // 10))
            jogo_ativo = False

        texto = fonte.render("Pressione 'k' para jogar", True, (255, 255, 255))
        janela.blit(texto, (LARGURA // 10 , ALTURA // 4))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
