import pygame
from pygame.locals import *
from sys import exit
import os 

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("imagens")

class Sapo(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        base = os.path.dirname(__file__) # Caminho da pasta do script

        self.sprites = []
        for i in range(1, 11):  # attack_1.png até attack_10.png
            self.sprites.append(pygame.image.load(os.path.join(base, f"attack_{i}.png")))
        
        self.atual = 0
        self.image = pygame.transform.scale(self.sprites[self.atual], (128*3, 64*3))
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

        self.atacando = False   # só permite um ataque por vez
    
    def atacar(self):
        if not self.atacando:   # só inicia se não estiver atacando
            self.atacando = True
            self.atual = 0
    
    def update(self):
        if self.atacando:
            self.atual += 0.5
            if self.atual >= len(self.sprites):
                self.atual = 0
                self.atacando = False  # terminou o ataque
            else:
                self.image = pygame.transform.scale(
                    self.sprites[int(self.atual)], (128*3, 64*3)
                )


todas_imagens = pygame.sprite.Group()
sapo = Sapo()
todas_imagens.add(sapo)

fps = 30
relogio = pygame.time.Clock()

while True:
    relogio.tick(fps)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        if evento.type == KEYDOWN:
            if evento.key == K_SPACE:
                sapo.atacar()  # só começa se não estiver atacando

    todas_imagens.update()

    tela.fill((0,0,0))
    todas_imagens.draw(tela)
    pygame.display.flip()
