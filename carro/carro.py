import pygame
import os 
from random import randint

pygame.init()

janela = pygame.display.set_mode((586, 600))
fonte = pygame.font.Font(None,32)
menu = True

while menu:
    pygame.display.flip()
    menu2 = fonte.render("Criando um jogo com Python", True, (200, 0, 0))
    menu3 = fonte.render("(A) Jogar", True, (200, 0, 0))
    menu4 = fonte.render("(E) Sair", True, (200, 0, 0))
    menu_comandos = pygame.key.get_pressed()
    if menu_comandos[pygame.K_a]:
        menu = False
        jogo_rodando_segundo_plano = True
    if menu_comandos[pygame.K_e]:
        menu = False
        jogo_rodando_segundo_plano = False
        
    janela.blit(menu2, (100, 10))
    janela.blit(menu3, (293, 100))
    janela.blit(menu4, (293, 190))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False

while jogo_rodando_segundo_plano:

    fim = False

    X = 300
    Y = 300

    XX = 200
    YY = 800

    XXX = 400
    YYY = 800

    velocidade = 10

    base_path = os.path.dirname(__file__)  # caminho da pasta do script

    fundo = pygame.image.load(os.path.join(base_path, "estrada.png")) # https://st.depositphotos.com/50990794/58191/v/450/depositphotos_581913586-stock-illustration-road-pixel-art-road-texture.jpg
    carro = pygame.image.load(os.path.join(base_path, "carro_1.png")) # https://www.vhv.rs/viewpic/mJbTwR_ios-icon-top-down-f1-car-png-transparent/
    carro2 = pygame.image.load(os.path.join(base_path, "carro_2.png"))
    carro3 = pygame.image.load(os.path.join(base_path, "carro_3.png"))

    carro = pygame.transform.scale(carro,(50, 50))
    carro2 = pygame.transform.scale(carro2,(50, 50))
    carro3 = pygame.transform.scale(carro3,(50, 50))
    fundo = pygame.transform.scale(fundo,(586, 600))

    pygame.display.set_caption("Criando um jogo com Python")

    cor=(0,0,0)

    janela_aberta = True
    ponto = 0
    while janela_aberta:
        janela.fill(cor)
        pygame.time.delay(50)

        if fim == False:
            ponto += 1
            pontos = fonte.render(f"ponto: {ponto}", False, (240,0,0))
        #f = coloca uma variavel dentro de aspas 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                janela_aberta = False
                jogo_rodando_segundo_plano = False

        #print(X, Y)
        comandos = pygame.key.get_pressed()
        if comandos[pygame.K_e]:
            janela_aberta = False
        if comandos[pygame.K_UP]:
            Y -= velocidade
            if Y == 10:
                Y += velocidade
        if comandos[pygame.K_DOWN]:
            Y += velocidade
            if Y == 550:
                Y -= velocidade
        if comandos[pygame.K_RIGHT]:
            X += velocidade
            if X == 420:
                X -= velocidade
        if comandos[pygame.K_LEFT]:
            X -= velocidade
            if X == 80:
                X += velocidade

        if (YY <= -200):
            YY = randint(800, 2000)
        if (YYY <= -200):
            YYY = randint(800, 2000)

        YY -= velocidade
        YYY -= velocidade
        
        #colisao
        colisao_player = pygame.draw.rect(janela, (200, 0, 0), (X,Y,50,50))
        colisao_carro2 = pygame.draw.rect(janela, (200, 0, 0), (XX,YY,50,50))
        colisao_carro3 = pygame.draw.rect(janela, (200, 0, 0), (XXX,YYY,50,50))
        if colisao_carro2.colliderect(colisao_player):
            fim = True
        if colisao_carro3.colliderect(colisao_player):
            fim = True

        janela.blit(fundo, (0, 0))
        janela.blit(pontos, (0, 0))
        janela.blit(carro, (X, Y))
        janela.blit(carro2, (XX, YY))
        janela.blit(carro3, (XXX, YYY))
        
        if fim == True:
            janela.fill(cor)
            pontos = fonte.render(f"ponto: {ponto}", False, (255,255,255))
            texto_final = fonte.render("Aperte E para recomeçar", False, (255,255,255))
            janela.blit(texto_final, (200, 300))
            janela.blit(pontos, (200, 200))

            if comandos[pygame.K_e]:
                janela_aberta = False

        pygame.display.update()
            
pygame.quit()
