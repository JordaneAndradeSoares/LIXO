import pygame
import sys
from random import randint

pygame.init()

LARGURA = 600
ALTURA = 600

tamanho = 40
tamanho_tiro = 10
tamanho_inimigo = 30
tamanho_da_fonte = 20
numero_de_inimigos = 10
velocidade_de_deslocamento = 10
velocidade_de_deslocamento_do_inimigo = 10

x_jogador = (LARGURA // 2) - (tamanho // 2)
y_jogador = ALTURA - tamanho - 10

jogo_ativo = False
verifica_se_perdeu_ao_menos_uma_vez = False

tiros = []
inimigos = []

teclas_press = {pygame.K_a: False, pygame.K_d: False}

clock = pygame.time.Clock()
fonte = pygame.font.SysFont('arial', tamanho_da_fonte, True, True)
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Super espacial")

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
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            novo_tiro = {'x': x_jogador + tamanho // 2 - tamanho_tiro // 2, 'y': y_jogador}
            tiros.append(novo_tiro)

        if teclas_press[pygame.K_a] and x_jogador > 0:
            x_jogador -= velocidade_de_deslocamento
        if teclas_press[pygame.K_d] and x_jogador < LARGURA - tamanho:
            x_jogador += velocidade_de_deslocamento

        pygame.draw.rect(janela, (255, 0, 0), (x_jogador, y_jogador, tamanho, tamanho))

        for tiro in tiros:
            tiro['y'] -= velocidade_de_deslocamento * 2
            pygame.draw.rect(janela, (255, 255, 255), (tiro['x'], tiro['y'], tamanho_tiro, tamanho_tiro))

        tiros = [tiro for tiro in tiros if tiro['y'] > -tamanho_tiro]
        inimigos = [inimigo for inimigo in inimigos if inimigo['y'] > -tamanho_inimigo]

        for inimigo in inimigos:
            inimigo['y'] += velocidade_de_deslocamento_do_inimigo
            pygame.draw.rect(janela, (0, 0, 255), (inimigo['x'], inimigo['y'], tamanho_inimigo, tamanho_inimigo))

            if inimigo['y'] > ALTURA:
                inimigo['y'] = 0

            for tiro in tiros:
                if (tiro['x'] < inimigo['x'] + tamanho_inimigo and
                        tiro['x'] + tamanho_tiro > inimigo['x'] and
                        tiro['y'] < inimigo['y'] + tamanho_inimigo and
                        tiro['y'] + tamanho_tiro > inimigo['y']):
                    tiros.remove(tiro)
                    inimigos.remove(inimigo)

            if (x_jogador < inimigo['x'] + tamanho_inimigo and
                    x_jogador + tamanho > inimigo['x'] and
                    y_jogador < inimigo['y'] + tamanho_inimigo and
                    y_jogador + tamanho > inimigo['y']):
                jogo_ativo = False
                verifica_se_perdeu_ao_menos_uma_vez = True

        if not inimigos:
            inimigos = [{'x': randint(0, LARGURA - tamanho_inimigo), 'y': 0} for _ in range(numero_de_inimigos)]

    if not jogo_ativo:
        x_jogador = (LARGURA // 2) - (tamanho // 2)
        y_jogador = ALTURA - tamanho - 10
        tiros = []

        if verifica_se_perdeu_ao_menos_uma_vez:
            texto_2 = fonte.render("Voce perdeu!", True, (255, 0, 0))
            janela.blit(texto_2, (LARGURA // 10 , ALTURA // 10))
            inimigos = []

        texto = fonte.render("Pressione 'k' para jogar", True, (255, 255, 255))
        janela.blit(texto, (LARGURA // 10 , ALTURA // 4))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
