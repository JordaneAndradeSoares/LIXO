import cv2
import numpy as np
import pygame
from scipy.optimize import linear_sum_assignment

def carregar_e_preparar(caminho, tamanho):
    imagem = cv2.imread(caminho)
    
    if imagem is None:
        raise ValueError(f"Não foi possível carregar a imagem: {caminho}")

    h, w = imagem.shape[:2]

    menor = min(h, w)
    inicio_x = (w - menor) // 2
    inicio_y = (h - menor) // 2
    imagem = imagem[inicio_y:inicio_y+menor, inicio_x:inicio_x+menor]

    # Aumentando o tamanho da imagem
    imagem = cv2.resize(imagem, (tamanho, tamanho))
    return imagem

def construir_matriz_custo(A, B, peso_proximidade=1.0):
    n = A.shape[0]

    A_flat = A.reshape(-1, 3)
    B_flat = B.reshape(-1, 3)

    custo_cor = np.linalg.norm(A_flat[:, None] - B_flat[None, :], axis=2)

    coords = np.indices((n, n)).reshape(2, -1).T
    custo_espacial = np.linalg.norm(coords[:, None] - coords[None, :], axis=2)

    return custo_cor + peso_proximidade * custo_espacial

def transformar(caminho_origem, caminho_alvo, tamanho=32, proximidade=0.5):
    origem = carregar_e_preparar(caminho_origem, tamanho)
    alvo = carregar_e_preparar(caminho_alvo, tamanho)

    custo = construir_matriz_custo(origem, alvo, proximidade)

    linhas, colunas = linear_sum_assignment(custo)

    # A imagem resultante é reconstruída com base na correspondência de pixels
    alvo_flat = alvo.reshape(-1, 3)
    resultado = alvo_flat[colunas].reshape(tamanho, tamanho, 3)

    return origem, alvo, resultado, linhas, colunas

def salvar_resultado(imagem, caminho="saida.png"):
    cv2.imwrite(caminho, imagem)

# Variaveis
caminho_origem = input("Digite o nome da imagem que quer recriar com sua extensão: ")
caminho_alvo = input("Digite o nome da imagem que quer usar como base com sua extensão: ")

# Aumentando o tamanho da imagem e da tela
tamanho = int(input("Digite o tamanho (recomendo 64 no maximo): "))  # Tamanho da imagem
zoom_da_imagem = 4 # Zoom para a imagem criada ficar maior na tela do pygame
proximidade = 0.2

# Inicializa pygame
pygame.init()

# Cria uma janela maior do pygame
screen = pygame.display.set_mode((tamanho * zoom_da_imagem, tamanho * zoom_da_imagem))  # Tamanho da janela
pygame.display.set_caption('Imagem')

# Exibição em tempo real durante o processamento
origem, alvo, resultado, linhas, colunas = transformar(caminho_origem, caminho_alvo, tamanho, proximidade)

# Cria um array vazio para armazenar a imagem parcial
imagem_parcial = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)

# Processo de transformação, passo a passo
for i in range(1, len(linhas) + 1):
    # A cada iteração, preenche a imagem parcial com os pixels correspondentes
    imagem_parcial_flat = imagem_parcial.reshape(-1, 3)
    imagem_parcial_flat[:i] = alvo.reshape(-1, 3)[colunas[:i]]
    imagem_parcial = imagem_parcial_flat.reshape(tamanho, tamanho, 3)

    # Converte a imagem para o formato do pygame (Surface)
    imagem_parcial_rgb = cv2.cvtColor(imagem_parcial, cv2.COLOR_BGR2RGB)
    imagem_parcial_surface = pygame.surfarray.make_surface(imagem_parcial_rgb)

    # Aplique o zoom na imagem gerada
    imagem_com_zoom = cv2.resize(imagem_parcial, (tamanho * zoom_da_imagem, tamanho * zoom_da_imagem))

   # Converte a imagem para o formato do pygame (Surface)
    imagem_com_zoom_rgb = cv2.cvtColor(imagem_com_zoom, cv2.COLOR_BGR2RGB)
    imagem_com_zoom_surface = pygame.surfarray.make_surface(imagem_com_zoom_rgb)

    # Atualiza a tela do pygame com a imagem modificada
    screen.blit(imagem_com_zoom_surface, (0, 0))
    pygame.display.flip()  # Atualiza a tela do pygame

# Salva o resultado final
salvar_resultado(resultado)

# Fechar pygame ao finalizar
pygame.quit()

print("Imagem gerada com sucesso: saida.png")