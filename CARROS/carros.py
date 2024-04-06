import pygame
from random import randint

def main_menu(screen):
    font = pygame.font.Font(None, 32)
    menu = True
    while menu:
        pygame.display.flip()
        screen.fill((0, 0, 0))
        menu_play = font.render("(A) Jogar", True, (225, 0, 0))
        menu_exit = font.render("(E) Sair", True, (225, 0, 0))
        screen.blit(menu_play, (293, 100))
        screen.blit(menu_exit, (293, 190))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
        menu_commands = pygame.key.get_pressed()
        if menu_commands[pygame.K_a]:
            menu = False
            return True
        if menu_commands[pygame.K_e]:
            menu = False
            return False

def game(screen):
    X, Y = 300, 300
    XX, YY = 200, 800
    XXX, YYY = 400, 800
    velocity = 10
    load = "C:\\Users\\Jordane A. Soares\\Pictures\\jogos\\codigos\\CARROS\\"
    background = pygame.image.load(f"{load}estrada.jpeg")
    car1 = pygame.transform.scale(pygame.image.load(f"{load}CARRO.jpeg"), (50, 50))
    car2 = pygame.transform.scale(pygame.image.load(f"{load}CARRO2.jpeg"), (50, 50))
    car3 = pygame.transform.scale(pygame.image.load(f"{load}CARRO3.jpeg"), (50, 50))
    background = pygame.transform.scale(background, (586, 600))
    cor = (0, 0, 0)
    screen_open = True
    score = 0

    while screen_open:
        screen.fill(cor)
        pygame.time.delay(50)
        score += 1
        score_text = font.render(f"Pontos: {score}", False, (0, 240, 0))
        screen.blit(background, (0, 0))
        screen.blit(score_text, (0, 0))
        screen.blit(car1, (X, Y))
        screen.blit(car2, (XX, YY))
        screen.blit(car3, (XXX, YYY))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_open = False

        commands = pygame.key.get_pressed()
        if commands[pygame.K_e]:
            screen_open = False
        if commands[pygame.K_UP] and Y > 10:
            Y -= velocity
        if commands[pygame.K_DOWN] and Y < 550:
            Y += velocity
        if commands[pygame.K_RIGHT] and X < 420:
            X += velocity
        if commands[pygame.K_LEFT] and X > 80:
            X -= velocity

        if YY <= -200:
            YY = randint(800, 2000)
        if YYY <= -200:
            YYY = randint(800, 2000)
        YY -= velocity
        YYY -= velocity

        col_player = pygame.Rect(X, Y, 50, 50)
        col_car2 = pygame.Rect(XX, YY, 50, 50)
        col_car3 = pygame.Rect(XXX, YYY, 50, 50)
        if col_car2.colliderect(col_player) or col_car3.colliderect(col_player):
            screen_open = False

        pygame.display.update()

    return score

pygame.init()
screen = pygame.display.set_mode((586, 600))
font = pygame.font.Font(None, 32)
running = True

while running:
    play = main_menu(screen)
    if play:
        score = game(screen)
        print("Pontuação:", score)
    else:
        running = False

pygame.quit()
