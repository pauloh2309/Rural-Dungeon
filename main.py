import pygame


janela = pygame.display.set_mode([720, 480])

pygame.display.set_caption('Rural Dungeon')

imagem_fundo = pygame.image.load('C:/Users/pauli/OneDrive/Documentos/Rural-Dungeon/imagens_game/ceagri menu.jpg')

loop = True

while loop:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            loop = False

    janela.blit(imagem_fundo, (0,0))

    pygame.display.update()


