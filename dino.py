import pygame
from random import choice
import sys

pygame.init()
LARGURA, ALTURA = 800, 400
tamanho = 50
posicao_jogador_x = LARGURA // 12
posicao_jogador_y = ALTURA - tamanho
posicao_obstaculo_x = LARGURA
velocidade_jogador = 7
salto_jogador = -400
pulando = False
agachado = False
contador_salto = 18
gravidade = 0.5
fonte_1 = pygame.font.Font(None, 36)
fonte_2 = pygame.font.Font(None, 20)
pontos = 0

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dino")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

clock = pygame.time.Clock()

jogo_ativo = True
a = ALTURA - tamanho
b = ALTURA - 1.5 * tamanho
posicao_obstaculo_y = choice([a, b])

while True:
    janela.fill(PRETO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_q and not agachado and not pulando:
                pulando = True
            if evento.key == pygame.K_e and not pulando:
                agachado = True
            if not jogo_ativo and evento.key == pygame.K_k:
                jogo_ativo = True
                posicao_jogador_y = ALTURA - tamanho
                posicao_obstaculo_x = LARGURA
                pontos = 0

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_e:
                agachado = False

    if posicao_obstaculo_y > LARGURA + tamanho:
        posicao_obstaculo_y = choice([ALTURA - tamanho, ALTURA - 2 * tamanho])

    if jogo_ativo:
        if pulando:
            if contador_salto >= -20:
                neg = 1
                if contador_salto < 0:
                    neg = -1
                posicao_jogador_y -= (contador_salto ** 2) * 0.03 * neg
                contador_salto -= 1
            else:
                pulando = False
                contador_salto = 18
        else:
            if posicao_jogador_y < ALTURA - tamanho and not agachado:
                posicao_jogador_y += gravidade

        if posicao_jogador_y >= ALTURA - tamanho:
            posicao_jogador_y = ALTURA - tamanho

        posicao_obstaculo_x -= 15

        if posicao_obstaculo_x < 0:
            posicao_obstaculo_x = LARGURA
            posicao_obstaculo_y = choice([a, b])

        if agachado:
            if pygame.Rect(posicao_jogador_x, posicao_jogador_y + tamanho // 2, tamanho, tamanho // 2).colliderect(
                    pygame.Rect(posicao_obstaculo_x, posicao_obstaculo_y, tamanho, tamanho)):
                jogo_ativo = False
        else:
            if pygame.Rect(posicao_jogador_x, posicao_jogador_y, tamanho, tamanho).colliderect(
                    pygame.Rect(posicao_obstaculo_x, posicao_obstaculo_y, tamanho, tamanho)):
                jogo_ativo = False

    if agachado:
        pygame.draw.rect(janela, BRANCO, (posicao_jogador_x, posicao_jogador_y + tamanho // 2, tamanho, tamanho // 2))
    else:
        pygame.draw.rect(janela, BRANCO, (posicao_jogador_x, posicao_jogador_y, tamanho, tamanho))

    pygame.draw.rect(janela, BRANCO, (posicao_obstaculo_x, posicao_obstaculo_y, tamanho, tamanho))

    if not jogo_ativo:
        texto_derrota = fonte_2.render(f"Você perdeu com {pontos} pontos", True, (255, 0, 0))
        text_rect = texto_derrota.get_rect(center=(LARGURA // 2, ALTURA // 2))
        janela.blit(texto_derrota, text_rect)
    else:
        texto_pontos = fonte_1.render(f"Pontos: {pontos}", True, BRANCO)
        text_rect = texto_pontos.get_rect(center=(LARGURA // 2, ALTURA // 2))
        janela.blit(texto_pontos, text_rect)
        pontos += 1

    pygame.display.update()
    clock.tick(30)
