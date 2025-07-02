import pygame
import random
import sys
import os

pygame.init()

# cores
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0) 
BRANCO = (255, 255, 255)

# tela e fonte 
LARGURA, ALTURA = 800, 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
fonte = pygame.font.SysFont("Arial", 40, True, True)

# pulo e booleanos
contador_salto = 10
salto_jogador = -10
pulando = False
jogando = False
resultado = True
contador_derrota = False

# outras variaveis 
clock = pygame.time.Clock()

velocidade_obstaculos = 10
numero_do_jogo = 1 
pontos = 0
fps = 60

tamanho = 50
jogador_x = 10
jogador_y = ALTURA - tamanho

obstaculo_x = LARGURA + tamanho
obstaculo_y = ALTURA - tamanho
obstaculo_y_reserva = obstaculo_y

obstaculo_voador_x = obstaculo_x
obstaculo_voador_y = ALTURA - (tamanho * 2.1)

# inimigo voador
class Rex_0(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        base_path = os.path.dirname(__file__)  # Caminho da pasta do script
        self.image_voadora = pygame.image.load(os.path.join(base_path, "4.png"))
        self.image_voadora = pygame.transform.scale(self.image_voadora, (tamanho * 2.6, tamanho))

        self.rect = self.image_voadora.get_rect()
        self.rect.topleft = 100, 100
    
# jogador
class Rex_1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        base_path = os.path.dirname(__file__)  # Caminho da pasta do script

        a1 = pygame.image.load(os.path.join(base_path, "1.png"))
        a2 = pygame.image.load(os.path.join(base_path, "2.png"))
        a3 = pygame.image.load(os.path.join(base_path, "3.png"))
        self.sprites = [a1, a2, a3]

        self.frame_count = 0
        self.frame_rate = 5
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100

    def update(self):
        self.frame_count += 1
        if self.frame_count % self.frame_rate == 0:
            self.atual += 1

            if self.atual >= len(self.sprites):
                self.atual = 0
            
            self.image = self.sprites[self.atual]
            self.image = pygame.transform.scale(self.image, (tamanho, tamanho))


# inimigo que anda
class Rex_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        base_path = os.path.dirname(__file__)  # Caminho da pasta do script

        a5 = pygame.image.load(os.path.join(base_path, "1.png"))
        a6 = pygame.image.load(os.path.join(base_path, "2.png"))
        a7 = pygame.image.load(os.path.join(base_path, "3.png"))
        self.sprites = [a5, a6, a7]

        self.sprites_invertidos = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]

        self.atual = 0
        self.image = self.sprites_invertidos[self.atual]
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

        self.frame_count = 0
        self.frame_rate = 5
        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100

    def update(self):
        self.frame_count += 1
        if self.frame_count % self.frame_rate == 0:
            self.atual += 1

            if self.atual >= len(self.sprites_invertidos):
                self.atual = 0

            self.image = self.sprites_invertidos[self.atual]
            self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

# pulo
class Pulando(pygame.sprite.Sprite):
    def som_do_pulo():
        base_path = os.path.dirname(__file__)  # Caminho da pasta do script
        som_salto = pygame.mixer.Sound(os.path.join(base_path, "smw_jump.wav"))
        som_salto.play()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        base_path = os.path.dirname(__file__)  # Caminho da pasta do script
        self.sprites.append(pygame.image.load(os.path.join(base_path, "1.png")))

        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100

    def update(self):
        self.atual += 0.5

        if self.atual >= len(self.sprites):
            self.atual = 0

        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

andando = pygame.sprite.Group()
rex = Rex_1()
andando.add(rex)

voando_inimigo = pygame.sprite.Group()
rex_inimigo_voador = Rex_0()
voando_inimigo.add(rex_inimigo_voador)

andando_inimigo = pygame.sprite.Group()
rex_inimigo = Rex_2()
andando_inimigo.add(rex_inimigo)

pulo = pygame.sprite.Group()
pulinho = Pulando()
pulo.add(pulinho)

while True: # loop de gameplay 
    tela.fill(BRANCO)
    clock.tick(fps)

    # Nome da janela na qual o jogo roda 
    pygame.display.set_caption("Amogus - Dinossauro do Chrome") 

    # comandos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
       
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if jogando and not pulando: # comando pulo
                    Pulando.som_do_pulo()
                    contador_salto = 10 
                    pulando = True 
                
                if not jogando: # controle da derrota 
                    jogando = True

                    if contador_derrota:
                        pontos = 0 # zernado os pontos quando recomeça o jogo 
                        numero_do_jogo += 1 # contando quantos jogos já tiveram
 
    # gameplay             
    if jogando:

        # Define o retângulo do jogador
        jogador_rect = pygame.Rect(jogador_x, jogador_y, tamanho, tamanho)

        # Define os retângulos dos obstáculos
        obstaculo_rect = pygame.Rect(obstaculo_x, obstaculo_y, tamanho, tamanho)
        obstaculo_voador_rect = pygame.Rect(obstaculo_voador_x, obstaculo_voador_y, tamanho * 2.6, tamanho)

        # Verifica as colisões
        if jogador_rect.colliderect(obstaculo_rect) or jogador_rect.colliderect(obstaculo_voador_rect):
            
            contador_derrota = True
            jogando = False

            # mandando os inimigos de novo para o começo da tela
            obstaculo_x = LARGURA + tamanho
            obstaculo_y = ALTURA - tamanho

            obstaculo_voador_x = obstaculo_x
            obstaculo_voador_y = ALTURA - (tamanho * 2.1)

        limite_obstaculo_x = -tamanho
        andando.update() 
        voando_inimigo.update()
        andando_inimigo.update()

        if pulando:    
            if contador_salto >= -10: 
                direcao = 1

                if contador_salto < 0:
                    direcao = -1
                    
                jogador_y -= (contador_salto ** 2) * 0.2 * direcao
                contador_salto -= 1

            else:
                pulando = False
        
        if obstaculo_x <= limite_obstaculo_x:
            resultado = random.choice([True, False])
            obstaculo_x = LARGURA
            pontos += 1
        
        if obstaculo_voador_x <= limite_obstaculo_x:
            resultado = random.choice([True, False])
            obstaculo_voador_x = LARGURA
            pontos += 1
        
        else:
            # colocando jogador na tela
            tela.blit(rex.image, (jogador_x, jogador_y))

            if resultado: 
                # colocando obstaculo corredor na tela
                obstaculo_x -= velocidade_obstaculos
                tela.blit(rex_inimigo.image, (obstaculo_x, obstaculo_y))
            else: 
                # colocando obstaculo voador na tela
                obstaculo_voador_x -= velocidade_obstaculos
                tela.blit(rex_inimigo_voador.image_voadora, (obstaculo_voador_x, obstaculo_voador_y))

        mensagem = f"Pontos: {pontos}"
        texto = fonte.render(mensagem, True, PRETO)
        tela.blit(texto, (LARGURA // 3, ALTURA // 10))

    else:
        if contador_derrota :
            mensagem_2 = f"Fim do jogo {numero_do_jogo}! Ponto(s): {pontos}"
            texto_2 = fonte.render(mensagem_2, True, VERMELHO)
            tela.blit(texto_2, (LARGURA // 10 , ALTURA // 10))

        mensagem = "Pressione espaço para jogar e pular"
        texto = fonte.render(mensagem, True, PRETO)
        tela.blit(texto, (LARGURA // 14, ALTURA // 4))

        # Resetando jogador
        jogador_y = ALTURA - tamanho
        contador_salto = 10
        pulando = False

    pygame.display.update()