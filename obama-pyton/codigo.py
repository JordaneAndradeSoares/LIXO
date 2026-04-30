import cv2
import numpy as np
import pygame
import threading
from queue import Queue
import os

# carregar e preparar imagem (cortar quadrado central e redimensionar)
def carregar_e_preparar(caminho, tamanho):
    img = cv2.imread(caminho)

    if img is None:
        raise ValueError(f"Erro ao carregar: {caminho}")

    h, w = img.shape[:2]
    m = min(h, w)

    x = (w - m) // 2
    y = (h - m) // 2

    img = img[y:y+m, x:x+m]
    img = cv2.resize(img, (tamanho, tamanho))

    return img

# transformar pixels
def gerar_transformacoes(origem, alvo, fila):
    A = origem.reshape(-1, 3)
    B = alvo.reshape(-1, 3)

    usados = set()

    for i in range(len(A)):
        dist = np.linalg.norm(B - A[i], axis=1)

        # evita repetir pixels (melhora visual)
        for u in usados:
            dist[u] = 1e9

        idx = np.argmin(dist)
        usados.add(idx)

        fila.put((i, idx))

    fila.put(None)  # sinal de fim

# função principal
origem_path = input("Imagem que será copiada (com extensão): ")  # imagem que será usada como alvo
alvo_path = input("Imagem que será transformada (com extensão): ")  # imagem que será transformada para parecer com a origem
tamanho = int(input("Tamanho (recomendo 128 no máximo): "))

proximidade = 2  # quanto a imagem que será transformada deve se aproximar da imagem que quer copiar
zoom = 2  # tamanho do zoom

origem = carregar_e_preparar(origem_path, tamanho)
alvo = carregar_e_preparar(alvo_path, tamanho)

# pygame
pygame.init()
screen = pygame.display.set_mode((tamanho * zoom, tamanho * zoom))  # tela do tamanho da imagem vezes o zoom
pygame.display.set_caption("Transformação em tempo real")

imagem_parcial = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)

fila = Queue()

# thread de cálculo
thread = threading.Thread(target=gerar_transformacoes, args=(origem, alvo, fila))
thread.start()

frames = []

running = True
finalizado = False

# Usando for no lugar de while (iterações baseadas no número de transformações)
while not finalizado:  # Enquanto não finalizar, continuar rodando
    # processa fila
    if not fila.empty():
        item = fila.get()

        if item is None:
            finalizado = True
        else:
            idx, j = item
            imagem_parcial.reshape(-1, 3)[idx] = alvo.reshape(-1, 3)[j]

    # converter para pygame
    img_rgb = cv2.cvtColor(imagem_parcial, cv2.COLOR_BGR2RGB)

    surface = pygame.surfarray.make_surface(img_rgb)

    # zoom
    surface = pygame.transform.scale(surface, (tamanho * zoom, tamanho * zoom))

    screen.blit(surface, (0, 0))
    pygame.display.flip()

    # Adiciona o frame para o GIF, se necessário
    frame = cv2.cvtColor(imagem_parcial, cv2.COLOR_BGR2RGB)
    frames.append(frame)

# final
pygame.quit()

# salvar a imagem (após fechar a janela do pygame)
imagem_parcial_bgr = cv2.cvtColor(imagem_parcial, cv2.COLOR_RGB2BGR)

cv2.imwrite("saida.png", imagem_parcial_bgr)

print("Imagem salva com sucesso!")
print("Processo concluído.")