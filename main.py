import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

#janela jogo
bottom_panel = 100
screen_windth = 800
screen_height = 630 + bottom_panel

tela = pygame.display.set_mode((screen_windth, screen_height))
pygame.display.set_caption("Rural Dungeon")


#carregar imagens
#backgound imagem de fundo
background_img = pygame.image.load('C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens_game/background_do_jogo.png').convert_alpha()
#painel img
painel_img = pygame.image.load('C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens_game/painel.png').convert_alpha()



#função para desenhar o background
def draw_bg():
    tela.blit(background_img, (0,0))

#função para desenhar o painel
def draw_painel():
    tela.blit(painel_img, (0, screen_height - bottom_panel))


#classe Personagem
class Personagem():
        def __init__(self, x, y, nome, vida, defesa, ataque, iniciativa, dinheiro, xp, estamina, encontrou_bowser=0):
            self.nome = nome
            self.defesa = defesa
            self.ataque = ataque
            self.vida = vida
            self.vidabase = vida
            self.ataquebase = ataque
            self.defesabase = defesa
            self.iniciativa = iniciativa
            self.dinheiro = dinheiro
            self.estamina = estamina
            self.estaminabase = estamina
            self.encontrou_bowser = encontrou_bowser
            self.alive = True
            img = pygame.image.load('C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/Frames das animações/personagem ocioso/frame_0_delay-0.2s.gif')
            self.image = pygame.transform.scale(img, (img.get_width() * 5, img.get_height() * 5))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def draw(self):
            tela.blit(self.image, self.rect)

jogador = Personagem(200, 470, 'Miguel', 80, 20, 30, 1, 30, 0, 80, 0)

class Inimigos(Personagem):
    def __init__(self, x, y, nome, vida, defesa, ataque, iniciativa, dinheiro=0, xp=0, estamina=0, encontrou_bowser=0):
       super().__init__(x, y, vida, defesa, ataque, iniciativa, dinheiro, xp, estamina, encontrou_bowser)

adm_boss = Inimigos(250, 500, 'Goblin da Administração', 130, 20, 40, 0, 0, 0, 0)

boss_sustentavel = Inimigos(250, 500, 'Robô Natureza', 140, 25, 45, 0, 0, 0, 0)

matematica_boss = Inimigos(250, 500, 'Mago Místico', 100, 15, 50, 0, 0, 0, 0)

boss_python = Inimigos(250, 500, 'Robô Robust Python', 180, 50, 65, 0, 0, 0, 0)

run = True
while run:

    clock.tick(fps)

    #desenhar background
    draw_bg()

    #desenhar painel
    draw_painel()

    #desenhar jogador

    jogador.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()        

pygame.quit()
