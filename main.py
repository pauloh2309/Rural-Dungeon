import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

#janela jogo
bottom_panel = 335
screen_windth = 1024
screen_height = 720 + bottom_panel

tela = pygame.display.set_mode((screen_windth, screen_height))
pygame.display.set_caption("Batalha")


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
    def __init__(self, x, y, nome, max_vida):
        pass



run = True
while run:

    clock.tick(fps)

    #desenhar background
    draw_bg()

    #dsenhar painel
    draw_painel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()        

pygame.quit()
