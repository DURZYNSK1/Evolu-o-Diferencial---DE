import pygame
import sys
import random
import copy

TAM_CELULA = 60
NUM_RAINHAS = 8
LARGURA = TAM_CELULA * NUM_RAINHAS
ALTURA = TAM_CELULA * NUM_RAINHAS + 50  # espaço extra para o botão


pygame.init()
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Problema das 8 Rainhas - Evolução Diferencial")


BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

font = pygame.font.SysFont(None, 36)

solucao = []

### ALGORITMO DE (EVOLUÇÃO DIFERENCIAL) ###
def criar_individuo():
    return [random.randint(0, 7) for _ in range(8)]

def fitness(individuo):
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def mutacao_diferencial(a, b, c, F=0.8):
    mutado = []
    for i in range(8):
        valor = int(round(a[i] + F * (b[i] - c[i])))
        mutado.append(max(0, min(7, valor)))  # limitar entre 0 e 7
    return mutado

def crossover_binario(mutado, alvo, CR=0.9):
    trial = []
    jrand = random.randint(0, 7)
    for i in range(8):
        if random.random() < CR or i == jrand:
            trial.append(mutado[i])
        else:
            trial.append(alvo[i])
    return trial

def evolucao_diferencial():
    populacao = [criar_individuo() for _ in range(100)]
    for geracao in range(1000):
        nova_pop = []
        for i in range(100):
            indices = list(range(100))
            indices.remove(i)
            a, b, c = random.sample(indices, 3)
            mutado = mutacao_diferencial(populacao[a], populacao[b], populacao[c])
            trial = crossover_binario(mutado, populacao[i])
            if fitness(trial) <= fitness(populacao[i]):
                nova_pop.append(trial)
            else:
                nova_pop.append(populacao[i])
        populacao = nova_pop
        melhor = min(populacao, key=fitness)
        if fitness(melhor) == 0:
            return melhor
    return melhor  # retorna o melhor mesmo que não seja perfeito

###INTERFACE GRÁFICA###
def desenhar_tabuleiro():
    for linha in range(NUM_RAINHAS):
        for coluna in range(NUM_RAINHAS):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            rect = pygame.Rect(coluna * TAM_CELULA, linha * TAM_CELULA, TAM_CELULA, TAM_CELULA)
            pygame.draw.rect(screen, cor, rect)

def desenhar_rainhas():
    for coluna, linha in enumerate(solucao):
        center_x = coluna * TAM_CELULA + TAM_CELULA // 2
        center_y = linha * TAM_CELULA + TAM_CELULA // 2
        radius = TAM_CELULA // 3
        pygame.draw.circle(screen, VERMELHO, (center_x, center_y), radius)

def desenhar_botao():
    botao_largura = 290
    botao_altura = 40
    botao_x = 10
    botao_y = ALTURA - 50
    botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)
    pygame.draw.rect(screen, AZUL, botao_rect)
    texto = font.render("Gerar Nova Solução (DE)", True, BRANCO)
    texto_rect = texto.get_rect(center=botao_rect.center)
    screen.blit(texto, texto_rect)
    return botao_rect

def main():
    global solucao
    clock = pygame.time.Clock()
    solucao = evolucao_diferencial()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(event.pos):
                    solucao = evolucao_diferencial()

        desenhar_tabuleiro()
        desenhar_rainhas()
        botao_rect = desenhar_botao()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
