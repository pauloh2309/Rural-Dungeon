import pygame
pygame.init()

# -----------------------------------------------------------
# CONFIGURAÇÃO DA TELA
# -----------------------------------------------------------
WIDTH, HEIGHT = 960, 640
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movimentação do Personagem")
clock = pygame.time.Clock()
FPS = 60

# -----------------------------------------------------------
# ⬇️ SUBSTITUA AQUI O FUNDO DO MAPA
# -----------------------------------------------------------
try:
    background = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens_game/corredor-escolar-vazio_165488-2954.jpg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((70, 120, 200))

# -----------------------------------------------------------
# ⬇️ CARREGAR FRAMES DO PERSONAGEM (6 direita, 6 esquerda)
# -----------------------------------------------------------

def load_frames(pasta, quantidade):
    frames = []
    for i in range(1, quantidade + 1):
        img = pygame.image.load(f"{pasta}/frame{i}.png").convert_alpha()
        frames.append(img)
    return frames

walk_right = load_frames("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/Personagens do Rural Dungeon/andando_pra_direita_gif", 6)
walk_left  = load_frames("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/Personagens do Rural Dungeon/andando_pra esquerda_frames_gif", 6)

# -----------------------------------------------------------
# CLASSE DO PERSONAGEM
# -----------------------------------------------------------
class Player:
    def __init__(self):
        self.x = 200
        self.y = 400
        self.speed = 4

        self.frame_index = 0
        self.frame_delay = 8  # controla velocidade da animação
        self.frame_counter = 0

        self.direction = "right"  # ou "left"
        self.is_moving = False

        self.image = walk_right[0]

    def update(self, keys):
        self.is_moving = False

        # Movimento e direção
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "right"
            self.is_moving = True

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "left"
            self.is_moving = True

        # Atualizar animação
        self.animate()

    def animate(self):
        if not self.is_moving:
            # parado no frame inicial
            self.frame_index = 0
            self.image = walk_right[0] if self.direction == "right" else walk_left[0]
            return

        # contador da animação
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % 6

        # seleciona frame
        if self.direction == "right":
            self.image = walk_right[self.frame_index]
        else:
            self.image = walk_left[self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


player = Player()

# -----------------------------------------------------------
# LOOP PRINCIPAL
# -----------------------------------------------------------
running = True
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    # DESENHAR
    window.blit(background, (0, 0))
    player.draw(window)

    pygame.display.update()

pygame.quit()
