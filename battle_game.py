import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UILabel, UITextBox, UIProgressBar
from pygame.rect import Rect

<<<<<<< Updated upstream
=======
# ------------------------------------------------------
# CONFIGURAÇÃO GERAL
# ------------------------------------------------------
>>>>>>> Stashed changes
WIDTH, HEIGHT = 960, 640
FPS = 60

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rural Dungeon")
clock = pygame.time.Clock()

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

<<<<<<< Updated upstream
=======
# ------------------------------------------------------
# SISTEMA DE ESTADOS
# ------------------------------------------------------
>>>>>>> Stashed changes
class GameState:
    def __init__(self, game):
        self.game = game
        self.ui_elements = []

    def enter(self): pass

    def exit(self):
        for el in self.ui_elements:
            try:
                el.kill()
            except:
                pass
        self.ui_elements = []

    def handle_event(self, event): pass
    def update(self, dt): pass
    def render(self, surface): pass


class Game:
    def __init__(self):
        self.running = True
        self.states = {}
        self.state = None

<<<<<<< Updated upstream
=======
        # Dados do player
>>>>>>> Stashed changes
        self.player = {
            "name": "Firerat",
            "hp": 100,
            "max_hp": 100
        }

<<<<<<< Updated upstream
=======
        # Dados do inimigo
>>>>>>> Stashed changes
        self.enemy = {
            "name": "Goblin Selvagem",
            "hp": 120,
            "max_hp": 120
        }

<<<<<<< Updated upstream
=======
        # Registrar telas
>>>>>>> Stashed changes
        self.register_state("menu", MenuState(self))
        self.register_state("battle", BattleState(self))

        self.change_state("menu")

    def register_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        if self.state:
            self.state.exit()
        self.state = self.states[name]
        self.state.enter()

    def quit(self):
        self.running = False

<<<<<<< Updated upstream
class MenuState(GameState):

    def enter(self):
        self.bg = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens_game/ceagri menu.jpg").convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.logo = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens_game/f183fbea-b22f-4728-ba31-1180764de368.jpg").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (350, 140))
=======
# ------------------------------------------------------
# MENU INICIAL
# ------------------------------------------------------
class MenuState(GameState):

    def enter(self):
        # Background
        self.bg = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens_game/ceagri menu.jpg").convert()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        # Logo
        self.logo = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens_game/f183fbea-b22f-4728-ba31-1180764de368.jpg").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (350, 140))

>>>>>>> Stashed changes
        self.logo_ui = UIImage(
            relative_rect=Rect((WIDTH//2 - 175, 40), (350, 140)),
            image_surface=self.logo,
            manager=manager
        )
        self.ui_elements.append(self.logo_ui)

<<<<<<< Updated upstream
=======
        # Botões
>>>>>>> Stashed changes
        self.btn_play = UIButton(
            Rect(WIDTH//2 - 100, 250, 200, 50),
            "JOGAR",
            manager=manager
        )
        self.ui_elements.append(self.btn_play)

        self.btn_options = UIButton(
            Rect(WIDTH//2 - 100, 320, 200, 50),
            "OPÇÕES",
            manager=manager
        )
        self.ui_elements.append(self.btn_options)

        self.btn_exit = UIButton(
            Rect(WIDTH//2 - 100, 390, 200, 50),
            "SAIR",
            manager=manager
        )
        self.ui_elements.append(self.btn_exit)

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:

            if event.ui_element == self.btn_play:
                self.game.change_state("battle")

            if event.ui_element == self.btn_exit:
                self.game.quit()

    def render(self, surface):
        surface.blit(self.bg, (0, 0))

<<<<<<< Updated upstream
class BattleState(GameState):

    def enter(self):
=======
# ------------------------------------------------------
# TELA DE BATALHA (ESTILO POKÉMON)
# ------------------------------------------------------
class BattleState(GameState):

    def enter(self):
        # ------------------------------------------------------
        # 🔥 BACKGROUND
        # ------------------------------------------------------
>>>>>>> Stashed changes
        try:
            self.battle_bg = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/imagens_game/corredor-da-escola-corredor-da-faculdade-ou-universidade_107791-2122.jpg").convert()
            self.battle_bg = pygame.transform.scale(self.battle_bg, (WIDTH, HEIGHT))
        except:
            self.battle_bg = pygame.Surface((WIDTH, HEIGHT))
            self.battle_bg.fill((80, 120, 80))

<<<<<<< Updated upstream
=======
        # ------------------------------------------------------
        # 🔥 SPRITE DO PLAYER
        # ------------------------------------------------------
>>>>>>> Stashed changes
        try:
            img = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/bloggif_frames_gif/frame-4.gif").convert_alpha()
            self.player_sprite = pygame.transform.scale(img, (250, 250))
        except:
            self.player_sprite = pygame.Surface((250, 250))
            self.player_sprite.fill((200, 80, 80))

<<<<<<< Updated upstream
=======
        # ------------------------------------------------------
        # 🔥 SPRITE DO INIMIGO
        # ------------------------------------------------------
>>>>>>> Stashed changes
        try:
            img = pygame.image.load("C:/Users/pauli/OneDrive/Documentos/GitHub/Rural-Dungeon/Personagens do Rural Dungeon/cca808b0-22bb-43e0-868d-28714d6c5a0f-removebg-preview.png").convert_alpha()
            self.enemy_sprite = pygame.transform.scale(img, (250, 250))
        except:
            self.enemy_sprite = pygame.Surface((250, 250))
            self.enemy_sprite.fill((80, 200, 80))

<<<<<<< Updated upstream
=======
        # ------------------------------------------------------
        # BARRAS DE VIDA (CRIAR AQUI!!!)
        # ------------------------------------------------------
>>>>>>> Stashed changes
        self.hp_player = UIProgressBar(
            Rect(100, 480, 300, 25),
            manager=manager
        )
        self.ui_elements.append(self.hp_player)

        self.hp_enemy = UIProgressBar(
            Rect(550, 80, 300, 25),
            manager=manager
        )
        self.ui_elements.append(self.hp_enemy)

<<<<<<< Updated upstream
        self.update_bars()

=======
        # Inicializa HP correto
        self.update_bars()

        # ------------------------------------------------------
        # CAIXA DE TEXTO
        # ------------------------------------------------------
>>>>>>> Stashed changes
        self.textbox = UITextBox(
            html_text="<b>A batalha começou!</b>",
            relative_rect=Rect(50, 520, 860, 100),
            manager=manager
        )
        self.ui_elements.append(self.textbox)

<<<<<<< Updated upstream
=======
        # ------------------------------------------------------
        # BOTÃO DE ATAQUE
        # ------------------------------------------------------
>>>>>>> Stashed changes
        self.btn_attack = UIButton(
            Rect(400, 430, 200, 50),
            "ATACAR",
            manager=manager
        )
        self.ui_elements.append(self.btn_attack)

<<<<<<< Updated upstream
    def update_bars(self):
=======
    # ------------------------------------------------------
    # 🔥 ATUALIZA BARRAS — VERSÃO 0.6.14
    # ------------------------------------------------------
    def update_bars(self):
        # valor deve ser entre 0.0 e 1.0
>>>>>>> Stashed changes
        player_percent = self.game.player["hp"] / self.game.player["max_hp"]
        enemy_percent = self.game.enemy["hp"] / self.game.enemy["max_hp"]

        self.hp_player.set_current_progress(player_percent)
        self.hp_enemy.set_current_progress(enemy_percent)

<<<<<<< Updated upstream
=======
    # ------------------------------------------------------
>>>>>>> Stashed changes
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_attack:
                self.player_attack()

<<<<<<< Updated upstream
=======
    # ------------------------------------------------------
>>>>>>> Stashed changes
    def player_attack(self):
        damage = 20
        self.game.enemy["hp"] -= damage
        if self.game.enemy["hp"] < 0:
            self.game.enemy["hp"] = 0

        self.update_bars()
        self.textbox.set_text(f"Você causou {damage} de dano!")

        pygame.time.set_timer(pygame.USEREVENT + 1, 900, True)

<<<<<<< Updated upstream
=======
    # ------------------------------------------------------
>>>>>>> Stashed changes
    def enemy_attack(self):
        damage = 18
        self.game.player["hp"] -= damage
        if self.game.player["hp"] < 0:
            self.game.player["hp"] = 0

        self.update_bars()
        self.textbox.set_text(f"O inimigo causou {damage} de dano!")
<<<<<<< Updated upstream
=======

    # ------------------------------------------------------
>>>>>>> Stashed changes
    def update(self, dt):
        for event in pygame.event.get(pygame.USEREVENT + 1):
            self.enemy_attack()

<<<<<<< Updated upstream
=======
    # ------------------------------------------------------
>>>>>>> Stashed changes
    def render(self, surface):
        surface.blit(self.battle_bg, (0, 0))
        surface.blit(self.player_sprite, (100, 250))
        surface.blit(self.enemy_sprite, (600, 150))

<<<<<<< Updated upstream
=======

# ------------------------------------------------------
# LOOP PRINCIPAL
# ------------------------------------------------------
>>>>>>> Stashed changes
game = Game()

while game.running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

        game.state.handle_event(event)
        manager.process_events(event)

    game.state.update(dt)
    manager.update(dt)

    game.state.render(window)
    manager.draw_ui(window)

    pygame.display.update()

pygame.quit()
