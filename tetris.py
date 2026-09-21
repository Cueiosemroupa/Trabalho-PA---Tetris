import pygame
import random

pygame.init()

LARGURA_BLOCO = 30
COLUNAS = 10
LINHAS = 20
LARGURA_TELA = COLUNAS * LARGURA_BLOCO
ALTURA_TELA = LINHAS * LARGURA_BLOCO

TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tetris diferenciado")

try:
    TEXTURA_BLOCO = pygame.image.load("textura.png")
    TEXTURA_BLOCO = pygame.transform.scale(TEXTURA_BLOCO, (LARGURA_BLOCO, LARGURA_BLOCO))
except Exception as e:
    print("Não foi possível carregar 'textura.png'. Usando cor sólida como alternativa.")
    TEXTURA_BLOCO = pygame.Surface((LARGURA_BLOCO, LARGURA_BLOCO))
    TEXTURA_BLOCO.fill((0, 200, 250))

PECAS = [
    [[1, 1, 1, 1]],  
    [[1, 1], [1, 1]],  
    [[0, 1, 0], [1, 1, 1]],  
    [[1, 0, 0], [1, 1, 1]],  
    [[0, 0, 1], [1, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 1, 0], [0, 1, 1]]   
]

class Peca:
    def __init__(self, x, y, formato):
        self.x = x
        self.y = y
        self.formato = formato

    def rotacionar(self):
        self.formato = [list(linha) for linha in zip(*self.formato[::-1])]

def criar_grade(blocos_fixos={}):
    grade = [[(0, 0, 0) for _ in range(COLUNAS)] for _ in range(LINHAS)]
    for (x, y) in blocos_fixos:
        grade[y][x] = 1
    return grade

def posicao_valida(peca, grade):
    posicoes_aceitas = [[(j, i) for j in range(COLUNAS) if grade[i][j] == (0, 0, 0)] for i in range(LINHAS)]
    posicoes_aceitas = [j for sub in posicoes_aceitas for j in sub]

    formatada = []
    for i, linha in enumerate(peca.formato):
        for j, col in enumerate(linha):
            if col == 1:
                formatada.append((peca.x + j, peca.y + i))

    for pos in formatada:
        if pos not in posicoes_aceitas:
            if pos[1] >= 0:
                return False
    return True

def limpar_linhas(grade, blocos_fixos):
    linhas_cheias = 0
    for i in range(LINHAS - 1, -1, -1):
        linha = grade[i]
        if (0, 0, 0) not in linha:
            linhas_cheias += 1
            for j in range(COLUNAS):
                del blocos_fixos[(j, i)]
            novos_blocos = {}
            for (x, y) in blocos_fixos:
                if y < i:
                    novos_blocos[(x, y + 1)] = True
                else:
                    novos_blocos[(x, y)] = True
            blocos_fixos.clear()
            blocos_fixos.update(novos_blocos)
    return linhas_cheias

def desenhar_grade_e_texturas(surface, grade, blocos_fixos, peca_atual):
    surface.fill((10, 10, 15))  

    for (x, y) in blocos_fixos:
        surface.blit(TEXTURA_BLOCO, (x * LARGURA_BLOCO, y * LARGURA_BLOCO))

    if peca_atual:
        for i, linha in enumerate(peca_atual.formato):
            for j, col in enumerate(linha):
                if col == 1:
                    px = (peca_atual.x + j) * LARGURA_BLOCO
                    py = (peca_atual.y + i) * LARGURA_BLOCO
                    surface.blit(TEXTURA_BLOCO, (px, py))

    for i in range(LINHAS):
        pygame.draw.line(surface, (40, 40, 40), (0, i * LARGURA_BLOCO), (LARGURA_TELA, i * LARGURA_BLOCO))
    for j in range(COLUNAS):
        pygame.draw.line(surface, (40, 40, 40), (j * LARGURA_BLOCO, 0), (j * LARGURA_BLOCO, ALTURA_TELA))

def main():
    blocos_fixos = {}
    grade = criar_grade(blocos_fixos)

    trocar_peca = False
    rodando = True
    peca_atual = Peca(3, 0, random.choice(PECAS))
    relogio = pygame.time.Clock()
    tempo_queda = 0
    velocidade_queda = 0.5  

    while rodando:
        grade = criar_grade(blocos_fixos)
        tempo_dt = relogio.tick(60) / 1000.0
        tempo_queda += tempo_dt

        if tempo_queda >= velocidade_queda:
            tempo_queda = 0
            peca_atual.y += 1
            if not posicao_valida(peca_atual, grade) and peca_atual.y > 0:
                peca_atual.y -= 1
                trocar_peca = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    peca_atual.x -= 1
                    if not posicao_valida(peca_atual, grade):
                        peca_atual.x += 1
                elif event.key == pygame.K_RIGHT:
                    peca_atual.x += 1
                    if not posicao_valida(peca_atual, grade):
                        peca_atual.x -= 1
                elif event.key == pygame.K_DOWN:
                    peca_atual.y += 1
                    if not posicao_valida(peca_atual, grade):
                        peca_atual.y -= 1
                elif event.key == pygame.K_UP:
                    peca_atual.rotacionar()
                    if not posicao_valida(peca_atual, grade):
                        for _ in range(3):
                            peca_atual.rotacionar()

        if trocar_peca:
            for i, linha in enumerate(peca_atual.formato):
                for j, col in enumerate(linha):
                    if col == 1:
                        blocos_fixos[(peca_atual.x + j, peca_atual.y + i)] = True
            peca_atual = Peca(3, 0, random.choice(PECAS))
            trocar_peca = False

            if not posicao_valida(peca_atual, grade):
                print("Game Over!")
                rodando = False

            limpar_linhas(grade, blocos_fixos)

        desenhar_grade_e_texturas(TELA, grade, blocos_fixos, peca_atual)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
