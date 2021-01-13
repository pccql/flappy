import pygame
from pygame.locals import *
from random import randint
from button_pygame import button

pygame.init()


def tela_inicial():
    largura = 400
    altura = 600
    screen = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Flappy Bird')
    inicio = True
    while inicio:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    inicio = False
        fundo = pygame.image.load('./images/fundo_flappy.png')
        fundo = pygame.transform.scale(fundo, (largura, altura))
        screen.blit(fundo, (0, 0))
        chao = pygame.image.load('./images/chao_flappy.png')
        chao = pygame.transform.scale(chao, (largura, 50))
        screen.blit(chao, (0, altura - chao.get_height()))

        font = pygame.font.Font(None, 80)
        titulo_text = font.render('Flappy Bird', True, (0, 0, 0))
        rect_titulo_texto = titulo_text.get_rect(center=(200, 250))
        screen.blit(titulo_text, rect_titulo_texto)

        if button(70, 'Jogar', (200, 400), 'black', 'white', screen, 'white', (255, 100, 0)):
            inicio = False

        pygame.display.flip()


def play():
    largura = 400
    altura = 600
    screen = pygame.display.set_mode((largura, altura))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    gravidade = 1
    velocity = 10
    tela_game_over = False
    imagens = ['./images/flappy_up.png', './images/flappy_mid.png',
               './images/flappy_down.png']

    class Jogador(pygame.sprite.Sprite):
        def __init__(self):
            super(Jogador, self).__init__()
            self.atual = 0
            self.surf = pygame.image.load(imagens[self.atual])
            self.rect = self.surf.get_rect(center=(200, 100))
            self.velocity = velocity

        def update(self):
            self.atual = (self.atual + 1) % 3
            self.surf = pygame.image.load(imagens[self.atual])
            self.velocity += gravidade
            self.rect[1] += self.velocity

        def pulo(self):
            self.velocity = -velocity

    class Cano(pygame.sprite.Sprite):
        def __init__(self):
            super(Cano, self).__init__()
            alturaCanoCima = randint(50, 350)
            alturaCanoBaixo = 450 - alturaCanoCima
            self.posY = 600 - alturaCanoBaixo
            self.surf_Cima = pygame.image.load('./images/cano_flappy.png')
            self.surf_Baixo = pygame.image.load('./images/cano_flappy.png')
            self.surf_Cima = pygame.transform.flip(self.surf_Cima, False, True)
            self.surf_Cima = pygame.transform.scale(self.surf_Cima, (40, alturaCanoCima))
            self.surf_Baixo = pygame.transform.scale(self.surf_Baixo, (40, alturaCanoBaixo))
            self.rectBaixo = self.surf_Baixo.get_rect(center=(450, self.posY + (self.surf_Baixo.get_height() // 2)))
            self.rectCima = self.surf_Cima.get_rect(center=(450, self.surf_Cima.get_height() // 2))

        def update(self):
            self.rectBaixo[0] -= 5
            self.rectCima[0] -= 5
            if self.rectCima.right < -10 or self.rectBaixo.right < -10:
                self.kill()
                grupo.remove(self)

    class Chao(pygame.sprite.Sprite):
        def __init__(self):
            super(Chao, self).__init__()
            self.surf = pygame.image.load('./images/chao_flappy.png')
            self.surf = pygame.transform.scale(self.surf, (largura, 50))
            self.rect = self.surf.get_rect(center=(600, 575))
            self.fakeRect = self.surf.get_rect(center=(200, 575))

    chao = Chao()
    grounds = pygame.sprite.Group()
    grounds.add(chao)
    ADD_CANO = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_CANO, 1400)
    jogador = Jogador()
    grupo = pygame.sprite.Group()
    contadorfake = 0
    contador = 0

    ADDCHAO = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCHAO, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_SPACE:
                    jogador.pulo()
            if event.type == ADD_CANO:
                cano = Cano()
                grupo.add(cano)
                contadorfake += 1
                if contadorfake > 1:
                    contador += 1
            if event.type == ADDCHAO:
                chao1 = Chao()
                grounds.add(chao1)

        fundo = pygame.image.load('./images/fundo_flappy.png')
        fundo = pygame.transform.scale(fundo, (largura, altura))
        screen.blit(fundo, (0, 0))

        screen.blit(jogador.surf, jogador.rect)
        jogador.update()
        if jogador.rect.top > 550:
            jogador.kill()
            tela_game_over = True
            running = False

        for i in grupo:
            screen.blit(i.surf_Cima, i.rectCima)
            screen.blit(i.surf_Baixo, i.rectBaixo)
            i.update()

            i.rect = i.rectBaixo
            if pygame.sprite.collide_rect(jogador, i):
                tela_game_over = True
                running = False
            i.rect = i.rectCima
            if pygame.sprite.collide_rect(jogador, i):
                tela_game_over = True
                running = False

        for i in grounds:
            screen.blit(i.surf, i.rect)
            i.rect[0] -= 5
            if i.rect.right < 0:
                i.kill()
                grounds.remove(i)
            if len(grounds) < 4:
                screen.blit(i.surf, i.fakeRect)
                i.fakeRect[0] -= 5
                if i.fakeRect.right < 0:
                    i.kill()
                    grounds.remove(i)

        font = pygame.font.Font(None, 40)
        textScore = font.render(f'Pontuação: {contador}', True, (0, 0, 0))
        textScoreRect = textScore.get_rect(center=(200, 50))
        screen.blit(textScore, textScoreRect)

        pygame.display.flip()
        clock.tick(30)

        while tela_game_over:
            for event in pygame.event.get():
                if event.type == QUIT:
                    tela_game_over = False
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    tela_game_over = False

            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 90)
            GameOver = font.render('Game Over', True, (255, 0, 0))
            GameOverRect = GameOver.get_rect(center=(200, 150))
            screen.blit(GameOver, GameOverRect)
            font = pygame.font.Font(None, 65)
            ScoreText = font.render(f'Pontuação: {contador}', True, (255, 255, 255))
            ScoreRect = ScoreText.get_rect(center=(200, 220))
            screen.blit(ScoreText, ScoreRect)

            if button(50, 'Play Again', (200, 360), 'black', 'white', screen, 'white', 'green'):
                play()
            if button(50, 'Sair', (200, 470), 'black', 'white', screen, 'white', 'red'):
                tela_game_over = False

            pygame.display.flip()

tela_inicial()
play()
