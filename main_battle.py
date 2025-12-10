import pygame
import os
import sys
import json

WIDTH, HEIGHT = 1024, 720

BASE_DIR = os.path.dirname(__file__)
VOLUME_FILE = os.path.join(BASE_DIR, 'volume_config.json')

def load_volume():
    """Carrega o volume salvo ou retorna 0.6 como padrão."""
    try:
        if os.path.exists(VOLUME_FILE):
            with open(VOLUME_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return max(0.0, min(1.0, float(data.get('volume', 0.6))))
    except Exception:
        pass
    return 0.6

def save_volume(volume):
    """Salva o volume atual."""
    try:
        with open(VOLUME_FILE, 'w', encoding='utf-8') as f:
            json.dump({'volume': max(0.0, min(1.0, volume))}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

current_game_volume = 0.6



def load_frames(path, scale=3):
    
    frames = []

    if not os.path.exists(path):
        print("Pasta não encontrada:", path)
        surf = pygame.Surface((50 * scale, 50 * scale), pygame.SRCALPHA)
        return [surf]

    def sort_key(fname):
        name = os.path.splitext(fname)[0]
        try:
            return int(name)
        except Exception:
            return name.lower()

    files = sorted(os.listdir(path), key=sort_key)

    for file in files:
        full = os.path.join(path, file)
        if not os.path.isfile(full):
            continue
        try:
            img = pygame.image.load(full).convert_alpha()
            w, h = img.get_width(), img.get_height()
            img = pygame.transform.scale(img, (w * scale, h * scale))
            frames.append(img)
        except Exception as exc:
            print(f"Falha ao carregar imagem {full}: {exc}")

    if not frames:
        surf = pygame.Surface((50 * scale, 50 * scale), pygame.SRCALPHA)
        return [surf]

    return frames


sounds = {}
music = None
current_heroi = None


class Fighter:
    def __init__(self, name, sprite_path, x, y, max_hp, attack, defense=0):
        self.name = name
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_power = attack
        self.defense = max(0, defense)
        self.special_charge = 0
        self.dead = False
        self.flip_horiz = False

        self.anim = {
            "idle": load_frames(sprite_path + "/idle"),
            "attack": load_frames(sprite_path + "/attack"),
            "hurt": load_frames(sprite_path + "/hurt"),
            "death": load_frames(sprite_path + "/death"),
        }

        self.state = "idle"
        self.frame = 0
        self.timer = 0
        self.frame_speed = 120
        self.trufas_used = 0

    def play(self, name):
        if self.state != name:
            self.state = name
            self.frame = 0
            self.timer = 0

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.timer > self.frame_speed:
            self.timer = now
            frames = self.anim[self.state]
            self.frame = (self.frame + 1) % len(frames)

            if self.state == "attack" and self.frame == len(frames) - 1:
                self.state = "idle"

            if self.state == "hurt" and self.frame == len(frames) - 1:
                self.state = "idle"

            if self.state == "death" and self.frame == len(frames) - 1:
                self.dead = True

    def draw(self, surf):
        img = self.anim[self.state][self.frame]
        if getattr(self, "flip_horiz", False):
            img = pygame.transform.flip(img, True, False)

        surf.blit(img, (self.x, self.y))

    def attack(self, target, special=False):
        self.play("attack")
        dmg = self.attack_power
        if special:
            dmg = int(dmg * 1.5)
            self.special_charge = 0

        defense_reduction = target.defense * 0.03
        dmg = max(1, int(dmg - defense_reduction))

        target.take_damage(dmg)
        self.special_charge = min(100, self.special_charge + 20)
        try:
            if self.name in ("Miguel", "Maria") and 'hit_jogador' in sounds:
                sounds['hit_jogador'].play()
        except Exception as exc:
            print(f"Erro ao tocar hit_jogador: {exc}")

    def take_damage(self, amount):
        self.hp -= amount
        self.special_charge = min(100, self.special_charge + 20)

        if self.hp <= 0:
            self.hp = 0
            self.play("death")
        else:
            self.play("hurt")


        try:
            if self.name in ("Miguel", "Maria") and amount > 0 and 'dano_inimigo' in sounds:
                sounds['dano_inimigo'].play()
        except Exception as exc:
            print(f"Erro ao tocar dano_inimigo: {exc}")

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)


class Button:
    def __init__(self, text, x, y):
        self.rect = pygame.Rect(x, y, 230, 50)
        self.text = text
        self.font = pygame.font.SysFont("Arial", 26)

    def draw(self, surf):
        pygame.draw.rect(surf, (40, 40, 40), self.rect, border_radius=8)
        pygame.draw.rect(surf, (200, 200, 200), self.rect, 2, border_radius=8)
        icon = getattr(self, "icon", None)
        if icon:
            icon_y = self.rect.y + (self.rect.height - icon.get_height()) // 2
            surf.blit(icon, (self.rect.x + 10, icon_y))
            text_x = self.rect.x + 10 + icon.get_width() + 8
        else:
            text_x = self.rect.x + 20

        txt = self.font.render(self.text, True, (255, 255, 255))
        txt_y = self.rect.y + (self.rect.height - txt.get_height()) // 2
        surf.blit(txt, (text_x, txt_y))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)




Fases = [
    ("Goblin_adm_oco", "backgrounds/bg_adm.png", 150),
    ("Robo_natureza_oco", "backgrounds/bg_sustent.png", 200),
    ("Mago_oco", "backgrounds/bg_mat.png", 240),
    ("robo_python", "backgrounds/bg_python.png", 280),
]

fase = 0


def carregar_fase():
    global player, enemy, background, fase

    nome, bg_file, hp = Fases[fase]
    background = pygame.image.load(bg_file).convert()

    try:
        hero_max = getattr(current_heroi, 'vidabase', None)
        hero_current = getattr(current_heroi, 'vida', None)
        hero_atk = getattr(current_heroi, 'ataquebase', getattr(current_heroi, 'ataque', None))
        hero_def = getattr(current_heroi, 'defesa', None)
        if hero_max is None:
            hero_max = hero_current
        if hero_max is None:
            hero_max = 120
        if hero_atk is None:
            hero_atk = 25
        if hero_def is None:
            hero_def = 0
        if hero_current is None:
            hero_current = hero_max
    except Exception:
        hero_max = 120
        hero_current = 120
        hero_atk = 25
        hero_def = 0

    try:
        choice = getattr(current_heroi, 'character', None)
    except Exception:
        choice = None

    if choice and str(choice).lower() == 'maria':
        player_name = "Maria"
        sprite_folder = "FramesAnimacoes/maria_oco"
    else:
        player_name = "Miguel"
        sprite_folder = "FramesAnimacoes/miguel_oco"

    player = Fighter(player_name, sprite_folder, 150, 300, hero_max, hero_atk, defense=hero_def)

    try:
        player.hp = max(0, min(player.max_hp, int(hero_current)))
    except Exception:
        player.hp = player.max_hp
    
    defesa_inimigo_map = {0: 0, 1: 1, 2: 2, 3: 3}
    defesa_inimigo = defesa_inimigo_map.get(fase, 0)
    
    enemy = Fighter(nome, f"FramesAnimacoes/{nome}", 650, 300, hp, 18, defense=defesa_inimigo)
    player.flip_horiz = False
    enemy.flip_horiz = True
    enemy.attack_power = max(1, int(enemy.attack_power * 0.7))
    player.trufas_used = 0
    if enemy.flip_horiz:
        for key, frames in enemy.anim.items():
            enemy.anim[key] = [pygame.transform.flip(img, True, False) for img in frames]

    print(f"Fase {fase}: player.flip_horiz={player.flip_horiz}, enemy.flip_horiz={enemy.flip_horiz}")

    if music:
        try:
            mixer.music.load(music)
            mixer.music.set_volume(0.85) 
            mixer.music.play(-1)
        except Exception as exc:
            print(f"Erro ao tocar música tema: {exc}")



def game_over_screen():
    title_font = pygame.font.SysFont("Arial", 64)
    font_timer = pygame.font.SysFont("Arial", 48)
    btn_retry = Button("Tentar Novamente", WIDTH // 2 - 220, HEIGHT // 2 + 80)
    btn_quit = Button("Desistir", WIDTH // 2 + 20, HEIGHT // 2 + 80)

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    timer_start = pygame.time.get_ticks()
    timer_duration = 10000

    while True:
        elapsed = pygame.time.get_ticks() - timer_start
        remaining_time = max(0, (timer_duration - elapsed) // 1000)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 'show_gameover'
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pos = e.pos
                if btn_retry.clicked(pos):
                    return 'retry'
                if btn_quit.clicked(pos):
                    return 'show_gameover'

        if remaining_time <= 0:
            return 'show_gameover'

        try:
            screen.blit(background, (0, 0))
        except Exception:
            screen.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = title_font.render("Game Over", True, (255, 0, 0))
        screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 2 - 120))

        timer_text = font_timer.render(f"Tempo: {remaining_time}s", True, (255, 255, 255))
        screen.blit(timer_text, ((WIDTH - timer_text.get_width()) // 2, HEIGHT // 2))

        btn_retry.draw(screen)
        btn_quit.draw(screen)

        pygame.display.update()
        clock.tick(60)


def show_gameover_image():
    try:
        gameover_sound = None
        try:
            gameover_sound_path = os.path.join(os.path.dirname(__file__), 'audios_game', 'gameover_som.mp3')
            if os.path.exists(gameover_sound_path):
                pygame.mixer.music.stop()
                gameover_sound = pygame.mixer.Sound(gameover_sound_path)
                gameover_sound.play()
        except Exception:
            pass
        
        gameover_path = os.path.join(os.path.dirname(__file__), 'imagens_game', 'gameover.jpg')
        if os.path.exists(gameover_path):
            gameover_img = pygame.image.load(gameover_path).convert()
            gameover_img = pygame.transform.smoothscale(gameover_img, (WIDTH, HEIGHT))
            screen.blit(gameover_img, (0, 0))
            pygame.display.update()
            pygame.time.wait(3000)
        else:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont("Arial", 48)
            text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(3000)
    except Exception as exc:
        print(f"Erro ao mostrar tela de game over: {exc}")
        pygame.time.wait(3000)


def pause_menu():
    global music
    title_font = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 20)
    
    btn_resume = Button("Continuar", WIDTH // 2 - 115, HEIGHT // 2 - 50)
    btn_quit_pause = Button("Sair", WIDTH // 2 - 115, HEIGHT // 2 + 20)
    
    volume_slider_x = WIDTH // 2 - 100
    volume_slider_y = HEIGHT // 2 - 120
    volume_slider_width = 200
    volume_slider_height = 20
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 'quit'

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return 'resume'
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pos = e.pos
                
                if (volume_slider_y <= pos[1] <= volume_slider_y + volume_slider_height and
                    volume_slider_x <= pos[0] <= volume_slider_x + volume_slider_width):
                    new_vol = (pos[0] - volume_slider_x) / volume_slider_width
                    mixer.music.set_volume(max(0.0, min(1.0, new_vol)))
                
                if btn_resume.clicked(pos):
                    return 'resume'

                if btn_quit_pause.clicked(pos):
                    return 'quit'
            
            if e.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                pos = e.pos
                if (volume_slider_y <= pos[1] <= volume_slider_y + volume_slider_height and
                    volume_slider_x <= pos[0] <= volume_slider_x + volume_slider_width):
                    new_vol = (pos[0] - volume_slider_x) / volume_slider_width
                    mixer.music.set_volume(max(0.0, min(1.0, new_vol)))
        
        try:
            screen.blit(background, (0, 0))
        except Exception:
            screen.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        title = title_font.render("PAUSADO", True, (255, 255, 255))
        screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 2 - 200))
        
        vol_label = font_small.render(f"Volume música: {int(mixer.music.get_volume() * 100)}%", True, (255, 255, 255))
        screen.blit(vol_label, (volume_slider_x, volume_slider_y - 30))
        
        pygame.draw.rect(screen, (100, 100, 100), (volume_slider_x, volume_slider_y, volume_slider_width, volume_slider_height))
        current_vol = mixer.music.get_volume()
        pygame.draw.rect(screen, (0, 200, 100), (volume_slider_x, volume_slider_y, volume_slider_width * current_vol, volume_slider_height))
        
        instructions = font_small.render("ESC para continuar | Clique no slider para ajustar volume", True, (200, 200, 200))
        screen.blit(instructions, ((WIDTH - instructions.get_width()) // 2, HEIGHT // 2 + 120))
        
        btn_resume.draw(screen)
        btn_quit_pause.draw(screen)
        
        pygame.display.update()
        clock.tick(60)


def run_battle(start_fase=0, heroi=None):
    global sounds, music, mixer, screen, clock, background, player, enemy, fase
    global current_heroi, current_game_volume
    current_heroi = heroi

    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        pass

    mixer = pygame.mixer
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rural Dungeon - Batalha")
    clock = pygame.time.Clock()

    # Carregar volume salvo
    current_game_volume = load_volume()
    if mixer.music.get_busy():
        mixer.music.set_volume(current_game_volume)

    if not sounds:
        try:
            sounds['dano_inimigo'] = mixer.Sound(os.path.join("audios_game", "hit_inimigo.mp3"))
            sounds['hit_jogador'] = mixer.Sound(os.path.join("audios_game", "hit_jogador.mp3"))
            sounds['cura_trufa'] = mixer.Sound(os.path.join("audios_game", "cura_trufa.mp3"))
            music = os.path.join("audios_game", "tema_batalha.mp3")
        except Exception as exc:
            print(f"Erro ao carregar áudios: {exc}")

    fase = start_fase
    trufa_icon = None
    try:
        trufa_path = os.path.join(os.path.dirname(__file__), 'trufa', 'trufa_icon.jpg')
        if os.path.exists(trufa_path):
            trufa_icon = pygame.image.load(trufa_path).convert_alpha()
            trufa_icon = pygame.transform.scale(trufa_icon, (32, 32))
    except Exception:
        trufa_icon = None

    # Carregar ícone de volume
    volume_icon = None
    try:
        volume_icon_path = os.path.join(os.path.dirname(__file__), 'imagens_game', 'opção_botão.png')
        if os.path.exists(volume_icon_path):
            volume_icon = pygame.image.load(volume_icon_path).convert_alpha()
            volume_icon = pygame.transform.scale(volume_icon, (40, 40))
    except Exception:
        pass

    btn_attack = Button("ATACAR", 50, 620)
    btn_special = Button("ESPECIAL", 350, 620)
    btn_trufa = Button("TRUFA", 650, 620)
    if trufa_icon:
        btn_trufa.icon = trufa_icon

    carregar_fase()

    turno_jogador = True
    esperando = False
    delay = 0

    font = pygame.font.SysFont("Arial", 24)

    while True:
        try:
            screen.blit(background, (0, 0))
        except Exception:
            screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (0, 0, 0), (0, 580, WIDTH, 140))

        pygame.draw.rect(screen, (180, 0, 0), (50, 600, 300, 20))
        pygame.draw.rect(screen, (0, 200, 0), (50, 600, 300 * (player.hp / player.max_hp), 20))
        screen.blit(font.render("HP Jogador", True, (255, 255, 255)), (50, 575))

        pygame.draw.rect(screen, (180, 0, 0), (650, 600, 300, 20))
        pygame.draw.rect(screen, (0, 200, 0), (650, 600, 300 * (enemy.hp / enemy.max_hp), 20))
        screen.blit(font.render("HP Inimigo", True, (255, 255, 255)), (650, 575))

        pygame.draw.rect(screen, (80, 80, 80), (350, 585, 230, 8))
        pygame.draw.rect(screen, (0, 120, 255), (350, 585, 230 * (player.special_charge / 100), 8))
        screen.blit(font.render("Especial", True, (255, 255, 255)), (350, 560))

        trufas_rest = max(0, 5 - getattr(player, 'trufas_used', 0))
        screen.blit(font.render(f"Trufas: {trufas_rest}/5", True, (255, 255, 255)), (650, 560))

        btn_attack.draw(screen)
        btn_special.draw(screen)
        btn_trufa.draw(screen)

        # Desenhar ícone de volume e controle
        volume_icon_rect = None
        if volume_icon:
            volume_icon_x = WIDTH - 60
            volume_icon_y = 20
            screen.blit(volume_icon, (volume_icon_x, volume_icon_y))
            volume_icon_rect = pygame.Rect(volume_icon_x, volume_icon_y, 40, 40)
        
        # Desenhar barra de volume quando houver clique próximo do ícone
        mouse_pos = pygame.mouse.get_pos()
        showing_volume = volume_icon_rect and volume_icon_rect.collidepoint(mouse_pos) if volume_icon_rect else False
        
        if showing_volume or True:  # Sempre mostrar a barra
            volume_bar_x = WIDTH - 200
            volume_bar_y = 25
            volume_bar_width = 150
            
            # Desenhar fundo da barra
            pygame.draw.rect(screen, (50, 50, 50), (volume_bar_x, volume_bar_y, volume_bar_width, 10), border_radius=5)
            
            # Desenhar barra preenchida
            fill_width = volume_bar_width * current_game_volume
            pygame.draw.rect(screen, (100, 255, 100), (volume_bar_x, volume_bar_y, fill_width, 10), border_radius=5)
            
            # Percentual de volume
            vol_font = pygame.font.SysFont(None, 16)
            vol_text = vol_font.render(f'{int(current_game_volume * 100)}%', True, (255, 255, 255))
            screen.blit(vol_text, (volume_bar_x - 30, volume_bar_y - 5))
        
        player.update()
        enemy.update()
        player.draw(screen)
        enemy.draw(screen)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 'quit'

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                res = pause_menu()
                if res == 'quit':
                    return 'quit'

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pos = e.pos
                
                # Controle de volume
                volume_bar_x = WIDTH - 200
                volume_bar_y = 25
                volume_bar_width = 150
                
                if (volume_bar_x <= pos[0] <= volume_bar_x + volume_bar_width and 
                    volume_bar_y - 5 <= pos[1] <= volume_bar_y + 15):
                    current_game_volume = (pos[0] - volume_bar_x) / volume_bar_width
                    current_game_volume = max(0.0, min(1.0, current_game_volume))
                    mixer.music.set_volume(current_game_volume)
                    # Ajustar som dos efeitos também
                    for sound in sounds.values():
                        if isinstance(sound, pygame.mixer.Sound):
                            sound.set_volume(current_game_volume)
                    save_volume(current_game_volume)
                elif turno_jogador:
                    if btn_attack.clicked(pos):
                        player.attack(enemy)
                        turno_jogador = False
                        esperando = True
                        delay = pygame.time.get_ticks()

                    if btn_trufa.clicked(pos):
                        if getattr(player, 'trufas_used', 0) < 5:
                            player.heal(30)
                            player.special_charge = min(100, player.special_charge + 20)
                            player.trufas_used += 1
                            turno_jogador = False
                            esperando = True
                            delay = pygame.time.get_ticks()
                            if 'cura_trufa' in sounds:
                                try:
                                    sounds['cura_trufa'].play()
                                except Exception as exc:
                                    print(f"Erro ao tocar cura_trufa: {exc}")
                        else:
                            print("Sem trufas restantes nesta luta.")

                    if btn_special.clicked(pos) and player.special_charge == 100:
                        player.attack(enemy, special=True)
                        turno_jogador = False
                        esperando = True
                        delay = pygame.time.get_ticks()

        if esperando and pygame.time.get_ticks() - delay > 700:
            esperando = False

            if not enemy.dead and not turno_jogador:
                enemy.attack(player)

            turno_jogador = True

        if enemy.dead:

            try:
                if current_heroi is not None:
                    current_heroi.vida = getattr(current_heroi, 'vidabase', player.max_hp)
            except Exception:
                pass
            mixer.music.stop()
            fase += 1
            return 'victory'

        if player.dead:
            mixer.music.stop()
            res = game_over_screen()
            if res == 'retry':
                try:
                    if current_heroi is not None:
                        current_heroi.vida = getattr(current_heroi, 'vidabase', getattr(current_heroi, 'vida', player.max_hp))
                except Exception:
                    pass
                # Reinicia a luta na mesma fase (não volta ao primeiro adversário)
                carregar_fase()
                turno_jogador = True
                esperando = False
                delay = 0
                continue
            if res == 'show_gameover':
                show_gameover_image()
                try:
                    if current_heroi is not None:
                        current_heroi.vida = player.hp
                except Exception:
                    pass
                return 'quit'

        pygame.display.update()
        clock.tick(60)
