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
velocidade_de_deslocamento_do_inimigo = 5

x_jogador = (LARGURA // 2) - (tamanho // 2)
y_jogador = ALTURA - tamanho - 10

jogo_ativo = False
verifica_se_perdeu_ao_menos_uma_vez = False

contador_tiros = 0
tempo_ultimo_aumento = pygame.time.get_ticks()

tiros = []
inimigos = []

# controles
teclas_press = {pygame.K_a: False, pygame.K_d: False, pygame.K_w: False}

clock = pygame.time.Clock()
fonte = pygame.font.SysFont('arial', tamanho_da_fonte, True, True)
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Nave espacial")

# Controle de tempo para spawn de inimigos
tempo_ultimo_inimigo = 0
intervalo_spawn = 2000  # 2000 milissegundos = 2 segundos

while True:
    janela.fill((0, 0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if not jogo_ativo and evento.key == pygame.K_SPACE:
                jogo_ativo = True
                verifica_se_perdeu_ao_menos_uma_vez = False
                inimigos = []
                tiros = []
                tempo_ultimo_inimigo = pygame.time.get_ticks()
                for _ in range(numero_de_inimigos):
                    inimigos.append({'x': randint(0, LARGURA - tamanho_inimigo), 'y': randint(-500, -50)})

            if evento.key in teclas_press:
                teclas_press[evento.key] = True

        if evento.type == pygame.KEYUP:
            if evento.key in teclas_press:
                teclas_press[evento.key] = False

    if jogo_ativo:
        tempo_atual = pygame.time.get_ticks()

        # Spawn automático de inimigos a cada intervalo
        if tempo_atual - tempo_ultimo_inimigo > intervalo_spawn:
            inimigos.append({'x': randint(0, LARGURA - tamanho_inimigo), 'y': 0})
            tempo_ultimo_inimigo = tempo_atual

        # Movimento do jogador
        if teclas_press[pygame.K_a] and x_jogador > 0:
            x_jogador -= velocidade_de_deslocamento
        if teclas_press[pygame.K_d] and x_jogador < LARGURA - tamanho:
            x_jogador += velocidade_de_deslocamento

        # Disparo
        if teclas_press[pygame.K_w]:
            if contador_tiros % 10 == 0:  # dispara a cada 10 frames
                novo_tiro = {'x': x_jogador + tamanho // 2 - tamanho_tiro // 2, 'y': y_jogador}
                tiros.append(novo_tiro)
            contador_tiros += 1
        else:
            contador_tiros = 0  # reseta o contador quando soltar a tecla W

        # Desenha o jogador
        pygame.draw.rect(janela, (255, 0, 0), (x_jogador, y_jogador, tamanho, tamanho))

        # Movimenta e desenha tiros
        for tiro in tiros:
            tiro['y'] -= velocidade_de_deslocamento * 2
            pygame.draw.rect(janela, (255, 255, 255), (tiro['x'], tiro['y'], tamanho_tiro, tamanho_tiro))

        tiros = [tiro for tiro in tiros if tiro['y'] > -tamanho_tiro]

        # Movimenta e desenha inimigos
        for inimigo in inimigos[:]:
            inimigo['y'] += velocidade_de_deslocamento_do_inimigo
            pygame.draw.rect(janela, (0, 0, 255), (inimigo['x'], inimigo['y'], tamanho_inimigo, tamanho_inimigo))

            # Se inimigo sair da tela, volta para o topo em posição aleatória
            if inimigo['y'] > ALTURA:
                inimigo['y'] = 0
                inimigo['x'] = randint(0, LARGURA - tamanho_inimigo)

            # Colisão tiro vs inimigo
            for tiro in tiros[:]:
                if (tiro['x'] < inimigo['x'] + tamanho_inimigo and
                    tiro['x'] + tamanho_tiro > inimigo['x'] and
                    tiro['y'] < inimigo['y'] + tamanho_inimigo and
                    tiro['y'] + tamanho_tiro > inimigo['y']):
                    try:
                        tiros.remove(tiro)
                        inimigos.remove(inimigo)
                    except ValueError:
                        pass

            # Colisão jogador vs inimigo
            if (x_jogador < inimigo['x'] + tamanho_inimigo and
                x_jogador + tamanho > inimigo['x'] and
                y_jogador < inimigo['y'] + tamanho_inimigo and
                y_jogador + tamanho > inimigo['y']):
                jogo_ativo = False
                verifica_se_perdeu_ao_menos_uma_vez = True

    # Tela de início ou derrota
    if not jogo_ativo:
        x_jogador = (LARGURA // 2) - (tamanho // 2)
        y_jogador = ALTURA - tamanho - 10
        tiros = []

        if verifica_se_perdeu_ao_menos_uma_vez:
            texto_2 = fonte.render("Voce perdeu!", True, (255, 0, 0))
            janela.blit(texto_2, (LARGURA // 10 , ALTURA // 10))

        texto = fonte.render("Pressione ESPACO para jogar", True, (255, 255, 255))
        janela.blit(texto, (LARGURA // 10 , ALTURA // 4))

        texto = fonte.render("Movimentacao: A e D", True, (255, 255, 255))
        janela.blit(texto, (LARGURA // 10 , int(ALTURA / 3.09)))

        texto = fonte.render("Disparo: W", True, (255, 255, 255))
        janela.blit(texto, (LARGURA // 10 , int(ALTURA / 2.5)))

    pygame.display.update()
    clock.tick(60)
