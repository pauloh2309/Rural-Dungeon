import pygame
from pygame.locals import *
from batalha import Batalha 

pygame.init()

LARGURA = 800
ALTURA = 500
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Rural Dungeon Battle")

fonte = pygame.font.Font(None, 32)
fonte_grande = pygame.font.Font(None, 42)

# ===========================
#   IMAGENS
# ===========================
background_batalha = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens_game/corredor bonito.png")
background_batalha = pygame.transform.scale(background_batalha, (LARGURA, ALTURA))

sprite_player = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/bloggif_frames_gif/frame-4.gif")
sprite_inimigo = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens/Felipe-removebg-preview.png")
sprite_inimigo = pygame.transform.scale(sprite_inimigo, (120, 120))


# ===========================
#   CAIXA DE STATUS
# ===========================
def desenhar_status_box(personagem, x, y, largura=220, altura=90):
    # Caixa
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura))
    pygame.draw.rect(tela, (255, 255, 255), (x, y, largura, altura), 3)

    hp = fonte.render(f"HP: {personagem.vida}/{personagem.vidabase}", True, (255, 255, 255))
    vigor = fonte.render(f"Vigor: {personagem.estamina}", True, (100, 200, 255))
    especial = fonte.render(f"Especial: {personagem.carga_especial}/{personagem.carga_max_especial}", True, (255, 215, 0))

    tela.blit(hp, (x + 10, y + 10))
    tela.blit(vigor, (x + 10, y + 35))
    tela.blit(especial, (x + 10, y + 60))


# ===========================
#   ANIMAÇÃO DE ATAQUE
# ===========================
def animacao_ataque(sprite, inicio, fim, duracao=200):
    clock = pygame.time.get_ticks()

    while pygame.time.get_ticks() - clock < duracao:
        tela.blit(background_batalha, (0, 0))
        tela.blit(sprite_player, (120, 300))
        tela.blit(sprite_inimigo, (550, 180))

        offset = 15 if (pygame.time.get_ticks() // 100) % 2 == 0 else -15
        tela.blit(sprite, (inicio[0] + offset, inicio[1]))

        pygame.display.update()


# ===========================
#   MENU
# ===========================
def desenhar_menu(opcao):
    opcoes = ["Ataque Básico", "Ataque Leve", "Ataque Pesado", "Defender", "Especial", "Usar Item"]
    y = 360

    for i, texto in enumerate(opcoes):
        cor = (255, 255, 0) if i == opcao else (255, 255, 255)
        t = fonte.render(texto, True, cor)
        tela.blit(t, (50, y + (i * 30)))


# ===========================
#   LOOP PRINCIPAL DA BATALHA
# ===========================
def iniciar_batalha(player, inimigo):
    batalha = Batalha()
    opcao = 0
    turno_do_player = True

    rodando = True
    ultimo_tick_estamina = pygame.time.get_ticks()

    while rodando:

        tela.blit(background_batalha, (0, 0))

        # Personagens mais próximos
        tela.blit(sprite_player, (120, 300))
        tela.blit(sprite_inimigo, (550, 180))

        # Status em caixas
        desenhar_status_box(player, 40, 30)
        desenhar_status_box(inimigo, 540, 30)

        desenhar_menu(opcao)

        pygame.display.update()

        # Recuperar estamina automaticamente
        if pygame.time.get_ticks() - ultimo_tick_estamina > 1200:
            if player.estamina < player.estaminabase:
                player.estamina += 1
            ultimo_tick_estamina = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                return

            if evento.type == KEYDOWN:

                if evento.key == K_UP:
                    opcao = (opcao - 1) % 6

                elif evento.key == K_DOWN:
                    opcao = (opcao + 1) % 6

                elif evento.key == K_RETURN:

                    if turno_do_player:

                        if opcao == 0:
                            animacao_ataque(sprite_player, (120, 300), (550, 180))
                            batalha.atacar_basico(player, inimigo)

                        elif opcao == 1:
                            animacao_ataque(sprite_player, (120, 300), (550, 180))
                            batalha.atacar_leve(player, inimigo)

                        elif opcao == 2:
                            animacao_ataque(sprite_player, (120, 300), (550, 180))
                            batalha.atacar_pesado(player, inimigo)

                        elif opcao == 3:
                            player.estamina += 2

                        elif opcao == 4:
                            animacao_ataque(sprite_player, (120, 300), (550, 180))
                            batalha.atacar_especial(player, inimigo)

                        elif opcao == 5:
                            batalha.usar_trufa(player)

                        turno_do_player = False

                    else:
                        animacao_ataque(sprite_inimigo, (550, 180), (120, 300))
                        batalha.atacar_leve(inimigo, player)
                        turno_do_player = True

        # Checar fim da batalha
        if inimigo.vida <= 0:
            print("Vitória!")
            rodando = False

        if player.vida <= 0:
            print("Derrota...")
            rodando = False



# ===========================
#   PERSONAGEM TEMPORÁRIO
# ===========================
class PersonagemTemp:
    def __init__(self, nome):
        self.nome = nome
        self.vida = 120
        self.vidabase = 120
        self.ataque = 30
        self.ataquebase = 30
        self.defesa = 10
        self.defesabase = 10
        self.estamina = 5
        self.estaminabase = 5
        self.carga_especial = 0
        self.carga_max_especial = 100
        self.trufa = [
            {"nome": "Trufa de morango", "qnt": 2, "descrição": "Cura 30 de vida"},
            {"nome": "Trufa de limão", "qnt": 1, "descrição": "Aumenta defesa em 20"}
        ]


# Rodar batalha
player = PersonagemTemp("Herói")
inimigo = PersonagemTemp("Goblin")

iniciar_batalha(player, inimigo)
