import pygame
from sys import exit
from random import randint

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
player_size = 50
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_vel_y = 0
pode_pular = False
pontos = 0
running = True
y2 = 0
x2 = randint(0, SCREEN_WIDTH - player_size)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Plataforma")

fonte = pygame.font.SysFont("Arial", 40, True, True)

while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player_vel_y += 1  
    y2 += 5  # Simula a queda do quadrado verde

    mensagem  = f"Pontos: {pontos}"
    texto = fonte.render(mensagem, True, (255, 255, 255))
    screen.blit(texto, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 10))

    if keys[pygame.K_SPACE] and pode_pular:
        player_vel_y = -15 
        pode_pular = False  

    player_x += 5 if keys[pygame.K_RIGHT] else 0
    player_x -= 5 if keys[pygame.K_LEFT] else 0

    player_y += player_vel_y
    if player_y + player_size > SCREEN_HEIGHT:
        player_y = SCREEN_HEIGHT - player_size
        player_vel_y = 0

    if player_x < 0:
        player_x = 0
    elif player_x > SCREEN_WIDTH - player_size:
        player_x = SCREEN_WIDTH - player_size

    if player_y < 0:
        player_y = 0
    elif player_y > SCREEN_HEIGHT - player_size:
        player_y = SCREEN_HEIGHT - player_size

    jogador = pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))
    terra = pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - player_size, SCREEN_WIDTH, player_size))
    plataforma = pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 3, SCREEN_HEIGHT - player_size * 3, SCREEN_WIDTH // 3, player_size))
    outro_retangulo = pygame.Rect(x2, y2, player_size, player_size)

    if jogador.colliderect(plataforma):
        pode_pular = True
        
        if player_vel_y > 0:
            player_y = plataforma.top - player_size
            player_vel_y = 0
        elif player_vel_y < 0:
            player_y = plataforma.bottom 

    if jogador.colliderect(terra):
        pode_pular = True
        
        if player_vel_y > 0:
            player_y = terra.top - player_size
            player_vel_y = 0

        elif player_vel_y < 0:
            player_y = terra.bottom 

    if jogador.colliderect(outro_retangulo):
        y2 = 0
        x2 = randint(0, SCREEN_WIDTH - player_size)
        pontos += 1

    if outro_retangulo.colliderect(plataforma) or outro_retangulo.colliderect(terra):
        y2 = 0
        x2 = randint(0, SCREEN_WIDTH - player_size)

    pygame.draw.rect(screen, WHITE, jogador)
    pygame.draw.rect(screen, WHITE, terra)
    pygame.draw.rect(screen, WHITE, plataforma)
    pygame.draw.rect(screen, (0, 255, 0), outro_retangulo)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
exit()
