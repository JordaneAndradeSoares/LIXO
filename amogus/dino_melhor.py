import pygame
import sys

pygame.init()

## cores
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0) 
BRANCO = (255, 255, 255)

## tela e fonte 
LARGURA, ALTURA = 800, 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
fonte = pygame.font.SysFont("Arial", 40, True, True)

## pulo e booleanos
contador_salto = 10
salto_jogador = -10
pulando = False
jogando = False
contador_derrota = False

## outras variaveis 
clock = pygame.time.Clock()

velocidade_do_obstaculo = 10
numero_do_jogo = 1 
pontos = 0
fps = 60

tamanho = 50
jogador_x = 10
obstaculo_x = LARGURA + tamanho

obstaculo_y = ALTURA - tamanho
jogador_y = ALTURA - tamanho
reserva = jogador_y

## primeira classe 
class Rex(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [
            pygame.image.load("C:\\Users\\Jordane AS\\Pictures\\codigos malucos\\amogus\\1.png"),
            pygame.image.load("C:\\Users\\Jordane AS\\Pictures\\codigos malucos\\amogus\\2.png"),
            pygame.image.load("C:\\Users\\Jordane AS\\Pictures\\codigos malucos\\amogus\\3.png")
        ]

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

## segunda classe
class Rex2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = [

            pygame.image.load("C:\\Users\\Jordane AS\\Pictures\\codigos malucos\\amogus\\1.png"),
            pygame.image.load("C:\\Users\\Jordane AS\\Pictures\\codigos malucos\\amogus\\2.png"),
            pygame.image.load("C:\\Users\\Jordane AS\\Pictures\\codigos malucos\\amogus\\3.png")
        ]

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

# terceira classe (pulando)
class Pulando(pygame.sprite.Sprite):
    def som_do_pulo():
        som_salto = pygame.mixer.Sound("C:\\Users\\Jordane AS\\Pictures\\codigos malucos\\amogus\\smw_jump.wav")
        som_salto.play()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load("C:\\Users\\Jordane AS\\Pictures\\codigos malucos\\amogus\\1.png"))
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
rex = Rex()
andando.add(rex)

andando_inimigo = pygame.sprite.Group()
rex_inimigo = Rex2()
andando_inimigo.add(rex_inimigo)

pulo = pygame.sprite.Group()
pulinho = Pulando()
pulo.add(pulinho)

## loop da gameplay 
while True:
    tela.fill(BRANCO)
    clock.tick(fps)

    # Nome da janela na qual o jogo roda 
    pygame.display.set_caption("Amogus - Dinossauro do Chrome") 

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
       
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_k and not pulando and jogando:
                pulando = True 
                contador_salto = 10 
                Pulando.som_do_pulo()
                
            elif evento.key == pygame.K_k and not jogando:
                jogando = True

                if contador_derrota:
                    numero_do_jogo += 1

                    """ uso -1 para resolver o problema do jogador ganhar um ponto do nada ao reiniciar, isso TALVEZ               
                    seja culpa do inimigo do jogo anterior terminar de passar ao começar um novo jogo e quando 
                    um inimigo passa pelo jogador isso é considerado um ponto para o jogador """
                    pontos = -1 
              
    if jogando:
        if obstaculo_x == jogador_x and obstaculo_y == jogador_y:
            jogando = False
            contador_derrota = True

        limite_obstaculo_x = -tamanho
        andando.update() 
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
            obstaculo_x = LARGURA
            pontos += 1
        
        else:
            obstaculo_x -= velocidade_do_obstaculo
            tela.blit(rex_inimigo.image, (obstaculo_x, obstaculo_y))
            tela.blit(rex.image, (jogador_x, jogador_y))

        mensagem = f"Pontos: {pontos}"
        texto = fonte.render(mensagem, True, PRETO)
        tela.blit(texto, (LARGURA // 3, ALTURA // 10))

    else:
        if contador_derrota :
            mensagem_2 = f"Fim do jogo {numero_do_jogo}! Ponto(s): {pontos}"
            texto_2 = fonte.render(mensagem_2, True, VERMELHO)
            tela.blit(texto_2, (LARGURA // 10 , ALTURA // 10))

        mensagem = "Pressione 'k' para jogar e pular"
        texto = fonte.render(mensagem, True, PRETO)
        tela.blit(texto, (LARGURA // 10 , ALTURA // 4))

    pygame.display.update()
