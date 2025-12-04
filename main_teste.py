

import json
import os
import time
import sys
import pygame
from pygame import Rect
from heroi import Heroi
from util import Util
import dialogo_pygame

SCREEN_W = 1024
SCREEN_H = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
BLUE = (40, 120, 200)

pygame.init()

try:
    pygame.mixer.init()
except Exception:
    pass

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Rural Dungeon")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y, color=BLACK):
    font = pygame.font.SysFont(None, size)
    txt = font.render(text, True, color)
    surface.blit(txt, (x, y))


class MenuButton:
    def __init__(self, rect, text, color=GRAY):
        self.rect = Rect(rect)
        self.text = text
        self.color = color

    def draw(self, surf, mouse_pos=None):
        shadow_rect = self.rect.move(4, 6)
        pygame.draw.rect(surf, (30, 30, 30), shadow_rect, border_radius=8)

        color = self.color
        if mouse_pos and self.rect.collidepoint(mouse_pos):
            color = tuple(min(255, c + 30) for c in color)

        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        font = pygame.font.SysFont(None, 28)
        text_surf = font.render(self.text, True, WHITE if color != GRAY else BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def save_heroi_to_file(heroi, path='save_heroi.json'):
    data = {
        'nome': heroi.nome,
        'vida': heroi.vida,
        'defesa': heroi.defesa,
        'ataque': heroi.ataque,
        'iniciativa': heroi.iniciativa,
        'estamina': heroi.estamina,
        'dinheiro': getattr(heroi, 'dinheiro', 0),
        'nivel': getattr(heroi, 'nivel', 1),
        'xp': getattr(heroi, 'xp', 0)
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_personagem_file(heroi, path='save_personagem.json'):
    data = {
        'nome': heroi.nome,
        'vida': heroi.vida,
        'defesa': heroi.defesa,
        'ataque': heroi.ataque,
        'iniciativa': heroi.iniciativa,
        'dinheiro': getattr(heroi, 'dinheiro', 10.5),
        'estamina': heroi.estamina,
        'interactions': getattr(heroi, 'interactions', [])
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_hero_individual(heroi, folder='heroes'):
    try:
        os.makedirs(folder, exist_ok=True)
        safe_name = ''.join(c for c in heroi.nome if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
        filename = f'{safe_name}_{int(time.time())}.json'
        path = os.path.join(folder, filename)
        data = {
            'nome': heroi.nome,
            'vida': heroi.vida,
            'defesa': heroi.defesa,
            'ataque': heroi.ataque,
            'iniciativa': heroi.iniciativa,
            'estamina': heroi.estamina,
            'dinheiro': getattr(heroi, 'dinheiro', 10.5),
            'nivel': getattr(heroi, 'nivel', 1),
            'xp': getattr(heroi, 'xp', 0)
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path
    except Exception:
        return None


def list_saved_heroes(folder='heroes'):
    res = []
    if not os.path.exists(folder):
        return res
    for name in sorted(os.listdir(folder)):
        if name.lower().endswith('.json'):
            path = os.path.join(folder, name)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                res.append((path, data))
            except Exception:
                continue
    return res

def hero_creation_screen(screen):
    clock_local = pygame.time.Clock()

    total_points = 120
    min_stat = 1
    stats = {
        'ataque': 1,
        'defesa': 1,
        'vida': 1,
        'iniciativa': 1,
        'estamina': 1
    }

    name = ''
    name_active = False

    buttons = {}
    start_x = 100
    start_y = 200
    gap_y = 60
    for i, key in enumerate(stats.keys()):
        y = start_y + i * gap_y
        buttons[f'{key}_minus'] = MenuButton((start_x + 300, y, 40, 32), '-')
        buttons[f'{key}_plus'] = MenuButton((start_x + 350, y, 40, 32), '+')

    confirm_btn = MenuButton((700, 600, 180, 50), 'Confirmar', GREEN)
    cancel_btn = MenuButton((880, 600, 100, 50), 'Voltar', RED)

    message = ''
    msg_timer = 0
    active_stat = None
    stat_inputs = {k: str(v) for k, v in stats.items()}

    cursor_timer = 0
    cursor_visible = True
    font_input = pygame.font.SysFont(None, 26)
    input_modal_active = False
    input_text = ''

    bg_img = None
    try:
        bg_path = os.path.join(os.path.dirname(__file__), 'imagens_game', 'ceagri menu.jpg')
        if os.path.exists(bg_path):
            bg_img = pygame.image.load(bg_path).convert()
            bg_img = pygame.transform.smoothscale(bg_img, (SCREEN_W, SCREEN_H))
    except Exception:
        bg_img = None

    running = True
    while running:
        clock_local.tick(FPS)
        cursor_timer += 1
        if cursor_timer >= 30:
            cursor_timer = 0
            cursor_visible = not cursor_visible
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for key in stats.keys():
                    if buttons[f'{key}_plus'].is_clicked(pos):
                        used = sum(int(stat_inputs[k]) if stat_inputs.get(k, '') != '' else 0 for k in stats.keys())
                        if used < total_points:
                            stats[key] += 1
                            stat_inputs[key] = str(stats[key])
                    if buttons[f'{key}_minus'].is_clicked(pos):
                        if stats[key] > min_stat:
                            stats[key] -= 1
                            stat_inputs[key] = str(stats[key])

                name_rect = Rect(50, 110, 400, 40)
                if name_rect.collidepoint(pos):
                    name_active = True
                    input_modal_active = False
                    input_text = ''
                else:
                    name_active = False

                for i, key in enumerate(stats.keys()):
                    y = start_x + i * gap_y  
                    y = start_y + i * gap_y
                    label_rect = Rect(start_x, y, 360, 32)
                    if label_rect.collidepoint(pos):
                        active_stat = key
                        stat_inputs[active_stat] = str(stats[active_stat])
                        input_modal_active = True
                        input_text = stat_inputs[active_stat]
                        message = f'Editando {active_stat}. Digite valor e pressione Enter.'
                        msg_timer = 120
                        break

                if confirm_btn.is_clicked(pos):
                    used = sum(stats.values())
                    if used != total_points:
                        message = f'Atribua todos os pontos: {used}/{total_points}'
                        msg_timer = 120
                    elif name.strip() == '':
                        message = 'Insira um nome para o herói.'
                        msg_timer = 120
                    else:
                        heroi = Heroi(nome=name.strip(), vida=stats['vida'], defesa=stats['defesa'],
                                      ataque=stats['ataque'], iniciativa=stats['iniciativa'],
                                      dinheiro_inicial=10.5, estamina=stats['estamina'])
                        save_heroi_to_file(heroi)
                        return heroi

                if cancel_btn.is_clicked(pos):
                    return None

            elif event.type == pygame.KEYDOWN:
                if input_modal_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        input_modal_active = False
                        input_text = ''
                    elif event.key == pygame.K_RETURN:
                        try:
                            newv = int(input_text) if input_text != '' else 0
                            if newv < min_stat:
                                message = 'Valor mínimo por atributo é 1.'
                                msg_timer = 120
                            else:
                                tentative = 0
                                for k in stat_inputs.keys():
                                    if k == active_stat:
                                        tentative += newv
                                    else:
                                        try:
                                            tentative += int(stat_inputs[k]) if stat_inputs.get(k, '') != '' else 0
                                        except Exception:
                                            tentative += stats[k]

                                stat_inputs[active_stat] = str(newv)
                                stats[active_stat] = newv
                                input_modal_active = False
                                input_text = ''
                        except ValueError:
                            message = 'Valor inválido. Digite apenas números.'
                            msg_timer = 120
                    else:
                        if event.unicode.isdigit() and len(input_text) < 4:
                            input_text += event.unicode
                else:
                    if name_active:
                        if event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            if len(name) < 20 and (event.unicode.isprintable()):
                                name += event.unicode

        if bg_img:
            screen.blit(bg_img, (0, 0))
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), flags=pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 40))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill((240, 245, 250))
            pygame.draw.rect(screen, (220, 235, 250), (0, 0, SCREEN_W, SCREEN_H // 3))

        pygame.draw.rect(screen, BLUE, (40, 20, SCREEN_W - 80, 80), border_radius=8)
        draw_text(screen, 'Criacao de Heroi', 40, 60, 30, color=WHITE)

        name_box_rect = Rect(50, 110, 400, 40)
        pygame.draw.rect(screen, (245, 245, 245), name_box_rect, border_radius=6)
        name_display = f'Nome: {name}'
        if cursor_visible and name_active and not input_modal_active:
            name_display += '_'
        draw_text(screen, name_display, 28, 60, 118)

        try:
            tentative = sum(int(stat_inputs[k]) if stat_inputs.get(k, '') != '' else 0 for k in stats.keys())
        except Exception:
            tentative = sum(stats.values())

        remaining = total_points - tentative
        draw_text(screen, f'Pontos usados: {tentative} / {total_points}', 24, 60, 160)
        rem_color = GREEN if remaining == 0 else RED
        draw_text(screen, f'Pontos restantes: {remaining}', 22, 60, 190, color=rem_color)

        for i, (key, val) in enumerate(stats.items()):
            y = start_y + i * gap_y
            label_rect = Rect(start_x, y, 240, 32)
            pygame.draw.rect(screen, (230, 230, 230), label_rect, border_radius=6)
            color_label = BLACK if active_stat != key else BLUE
            draw_text(screen, f'{key.capitalize()}:', 26, start_x + 8, y + 4, color=color_label)
            val_text = stat_inputs[key] if active_stat == key else str(val)
            txt_surf = font_input.render(val_text, True, BLACK)
            screen.blit(txt_surf, (start_x + 160, y + 4))
            if active_stat == key and cursor_visible:
                cursor_x = start_x + 160 + txt_surf.get_width() + 6
                pygame.draw.rect(screen, BLACK, (cursor_x, y + 8, 2, 20))

            bar_x = start_x + 420
            bar_w = 380
            pct = val / total_points
            pygame.draw.rect(screen, (200, 200, 200), (bar_x, y + 4, bar_w, 24), border_radius=6)
            pygame.draw.rect(screen, GREEN, (bar_x, y + 4, int(bar_w * pct), 24), border_radius=6)

            buttons[f'{key}_minus'].draw(screen)
            buttons[f'{key}_plus'].draw(screen)

        confirm_btn.draw(screen)
        cancel_btn.draw(screen)

        if input_modal_active and active_stat:
            modal_w = 520
            modal_h = 140
            mx = (SCREEN_W - modal_w) // 2
            my = (SCREEN_H - modal_h) // 2
            modal = pygame.Surface((modal_w, modal_h), flags=pygame.SRCALPHA)
            modal.fill((10, 10, 10, 220))
            screen.blit(modal, (mx, my))
            draw_text(screen, f'Insira o valor para {active_stat.capitalize()}:', 24, mx + 20, my + 18, color=WHITE)
            pygame.draw.rect(screen, (245, 245, 245), (mx + 20, my + 56, modal_w - 40, 40), border_radius=6)
            input_display = input_text if input_text != '' else stat_inputs.get(active_stat, '')
            txt_surf = font_input.render(input_display + ('_' if cursor_visible else ''), True, BLACK)
            screen.blit(txt_surf, (mx + 28, my + 64))

        if message:
            modal_w = 640
            modal_h = 80
            mx = (SCREEN_W - modal_w) // 2
            my = SCREEN_H - modal_h - 40
            modal_surf = pygame.Surface((modal_w, modal_h), flags=pygame.SRCALPHA)
            modal_surf.fill((0, 0, 0, 200))
            screen.blit(modal_surf, (mx, my))
            draw_text(screen, message, 26, mx + 20, my + 24, color=WHITE)
            msg_timer -= 1
            if msg_timer <= 0:
                message = ''

        pygame.display.flip()

    return None

def hero_selection_screen(screen):
    clock_local = pygame.time.Clock()
    files = list_saved_heroes()
    offset_y = 140
    running = True
    while running:
        clock_local.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for i, (path, data) in enumerate(files):
                    y = offset_y + i * 84
                    box = Rect(60, y, SCREEN_W - 120, 72)
                    if box.collidepoint(pos):
                        try:
                            h = Heroi(nome=data.get('nome',''), vida=data.get('vida',1),
                                      defesa=data.get('defesa',1), ataque=data.get('ataque',1),
                                      iniciativa=data.get('iniciativa',0),
                                      dinheiro_inicial=data.get('dinheiro',10.5),
                                      estamina=data.get('estamina',1))
                            return h
                        except Exception:
                            continue
                if Rect(880, 40, 100, 40).collidepoint(pos):
                    return None

        screen.fill((18,18,30))
        draw_text(screen, 'Selecionar Heroi', 44, 40, 30, color=WHITE)
        if not files:
            draw_text(screen, 'Nenhum herói salvo encontrado.', 28, 60, offset_y, color=WHITE)
            draw_text(screen, 'Crie um herói primeiro.', 20, 60, offset_y + 40, color=WHITE)
        else:
            for i, (path, data) in enumerate(files):
                y = offset_y + i * 84
                box = Rect(60, y, SCREEN_W - 120, 72)
                pygame.draw.rect(screen, (40,40,60), box, border_radius=8)
                draw_text(screen, data.get('nome','?'), 28, box.x + 12, box.y + 8, color=WHITE)
                info = f"Vida: {data.get('vida',1)}  Ataque: {data.get('ataque',1)}  Defesa: {data.get('defesa',1)}"
                draw_text(screen, info, 20, box.x + 12, box.y + 38, color=(200,200,200))

        back_btn = MenuButton((880, 40, 100, 40), 'Voltar', RED)
        mx,my = pygame.mouse.get_pos()
        back_btn.draw(screen, mouse_pos=(mx,my))

        pygame.display.flip()

    return None

def start_battle_with_heroi(heroi):
    WIDTH = SCREEN_W
    HEIGHT = SCREEN_H

    def load_frames_local(path, scale=3):
        frames = []
        if not os.path.exists(path):
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

    sounds_local = {}
    music_path = None
    try:
        sounds_local['dano_inimigo'] = pygame.mixer.Sound(os.path.join("audios_game", "hit_inimigo.mp3"))
        sounds_local['hit_jogador'] = pygame.mixer.Sound(os.path.join("audios_game", "hit_jogador.mp3"))
        sounds_local['cura_trufa'] = pygame.mixer.Sound(os.path.join("audios_game", "cura_trufa.mp3"))
        music_path = os.path.join("audios_game", "tema_batalha.mp3")
    except Exception as exc:
        print(f"Erro ao carregar áudios (batalha): {exc}")

    class FighterLocal:
        def __init__(self, name, sprite_path, x, y, max_hp, attack):
            self.name = name
            self.x = x
            self.y = y
            self.max_hp = max_hp
            self.hp = max_hp
            self.attack_power = attack
            self.special_charge = 0
            self.dead = False
            self.flip_horiz = False

            self.anim = {
                "idle": load_frames_local(sprite_path + "/idle"),
                "attack": load_frames_local(sprite_path + "/attack"),
                "hurt": load_frames_local(sprite_path + "/hurt"),
                "death": load_frames_local(sprite_path + "/death"),
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
                frames = self.anim.get(self.state, self.anim['idle'])
                self.frame = (self.frame + 1) % len(frames)
                if self.state in ("attack", "hurt") and self.frame == len(frames) - 1:
                    self.state = "idle"
                if self.state == "death" and self.frame == len(frames) - 1:
                    self.dead = True

        def draw(self, surf):
            frames = self.anim.get(self.state, self.anim['idle'])
            img = frames[self.frame]
            if getattr(self, "flip_horiz", False):
                img = pygame.transform.flip(img, True, False)
            surf.blit(img, (self.x, self.y))

        def attack(self, target, special=False):
            self.play("attack")
            dmg = self.attack_power
            if special:
                dmg = int(dmg * 1.5)
                self.special_charge = 0

            target.take_damage(dmg)
            self.special_charge = min(100, self.special_charge + 20)

            if "Miguel" in self.name and 'hit_jogador' in sounds_local:
                try:
                    sounds_local['hit_jogador'].play()
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

            if "Miguel" in self.name and amount > 0 and 'dano_inimigo' in sounds_local:
                try:
                    sounds_local['dano_inimigo'].play()
                except Exception as exc:
                    print(f"Erro ao tocar dano_inimigo: {exc}")

        def heal(self, amount):
            self.hp = min(self.max_hp, self.hp + amount)

    class BattleButton:
        def __init__(self, text, x, y):
            self.rect = pygame.Rect(x, y, 230, 50)
            self.text = text
            self.font = pygame.font.SysFont("Arial", 26)
            self.icon = None

        def draw(self, surf):
            pygame.draw.rect(surf, (40, 40, 40), self.rect, border_radius=8)
            pygame.draw.rect(surf, (200, 200, 200), self.rect, 2, border_radius=8)
            if self.icon:
                icon_y = self.rect.y + (self.rect.height - self.icon.get_height()) // 2
                surf.blit(self.icon, (self.rect.x + 10, icon_y))
                text_x = self.rect.x + 10 + self.icon.get_width() + 8
            else:
                text_x = self.rect.x + 20
            txt = self.font.render(self.text, True, (255, 255, 255))
            txt_y = self.rect.y + (self.rect.height - txt.get_height()) // 2
            surf.blit(txt, (text_x, txt_y))

        def clicked(self, pos):
            return self.rect.collidepoint(pos)

    trufa_icon = None
    try:
        trufa_icon = pygame.image.load(os.path.join("trufa", "trufa_icon.jpg")).convert_alpha()
        trufa_icon = pygame.transform.scale(trufa_icon, (32, 32))
    except Exception:
        trufa_icon = None

    Fases_local = [
        ("Goblin_adm_oco", "backgrounds/bg_adm.png", 150),
        ("Robo_natureza_oco", "backgrounds/bg_sustent.png", 200),
        ("Mago_oco", "backgrounds/bg_mat.png", 240),
        ("robo_python", "backgrounds/bg_python.png", 280),
    ]

    fase_idx = 0

    def carregar_fase_local():
        nonlocal player_local, enemy_local, background_local, fase_idx
        nome, bg_file, hp = Fases_local[fase_idx]
        try:
            background_local = pygame.image.load(bg_file).convert()
        except Exception:
            background_local = pygame.Surface((WIDTH, HEIGHT))
            background_local.fill((20, 20, 40))

        player_local = FighterLocal(heroi.nome, "FramesAnimacoes/miguel_oco", 150, 220, max(1, int(heroi.vida)), max(1, int(heroi.ataque)))
        enemy_local = FighterLocal(nome, f"FramesAnimacoes/{nome}", 650, 220, hp, 18)

        player_local.flip_horiz = False
        enemy_local.flip_horiz = True

        enemy_local.attack_power = max(1, int(enemy_local.attack_power * 0.7))
        player_local.trufas_used = 0

        if enemy_local.flip_horiz:
            for key, frames in enemy_local.anim.items():
                enemy_local.anim[key] = [pygame.transform.flip(img, True, False) for img in frames]

        if music_path:
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.85)
                pygame.mixer.music.play(-1)
            except Exception as exc:
                print(f"Erro ao tocar música tema: {exc}")

    player_local = None
    enemy_local = None
    background_local = None
    carregar_fase_local()

    btn_attack = BattleButton("ATACAR", 50, HEIGHT - 140)
    btn_special = BattleButton("ESPECIAL", 350, HEIGHT - 140)
    btn_trufa = BattleButton("TRUFA", 650, HEIGHT - 140)
    if trufa_icon:
        btn_trufa.icon = trufa_icon

    turno_jogador = True
    esperando = False
    delay = 0
    font_local = pygame.font.SysFont("Arial", 24)

    running_local = True
    while running_local:
        try:
            screen.blit(background_local, (0, 0))
        except Exception:
            screen.fill((10, 10, 30))

        pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT - 200, WIDTH, 200))
        pygame.draw.rect(screen, (180, 0, 0), (50, HEIGHT - 180, 300, 20))
        pygame.draw.rect(screen, (0, 200, 0), (50, HEIGHT - 180, 300 * (player_local.hp / max(1, player_local.max_hp)), 20))
        screen.blit(font_local.render(f"HP {player_local.name}", True, WHITE), (50, HEIGHT - 205))
        pygame.draw.rect(screen, (180, 0, 0), (600, HEIGHT - 180, 300, 20))
        pygame.draw.rect(screen, (0, 200, 0), (600, HEIGHT - 180, 300 * (enemy_local.hp / max(1, enemy_local.max_hp)), 20))
        screen.blit(font_local.render(f"HP {enemy_local.name}", True, WHITE), (600, HEIGHT - 205))
        pygame.draw.rect(screen, (80, 80, 80), (350, HEIGHT - 225, 230, 8))
        pygame.draw.rect(screen, (0, 120, 255), (350, HEIGHT - 225, 230 * (player_local.special_charge / 100), 8))
        screen.blit(font_local.render("Especial", True, WHITE), (350, HEIGHT - 250))
        trufas_rest = max(0, 5 - getattr(player_local, 'trufas_used', 0))
        screen.blit(font_local.render(f"Trufas: {trufas_rest}/5", True, WHITE), (650, HEIGHT - 260))

        btn_attack.draw(screen)
        btn_special.draw(screen)
        btn_trufa.draw(screen)

        player_local.update()
        enemy_local.update()
        player_local.draw(screen)
        enemy_local.draw(screen)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and turno_jogador:
                pos = e.pos
                if btn_attack.clicked(pos):
                    player_local.attack(enemy_local)
                    turno_jogador = False
                    esperando = True
                    delay = pygame.time.get_ticks()
                if btn_trufa.clicked(pos):
                    if getattr(player_local, 'trufas_used', 0) < 5:
                        player_local.heal(30)
                        player_local.special_charge = min(100, player_local.special_charge + 20)
                        player_local.trufas_used += 1
                        turno_jogador = False
                        esperando = True
                        delay = pygame.time.get_ticks()
                        if 'cura_trufa' in sounds_local:
                            try:
                                sounds_local['cura_trufa'].play()
                            except Exception:
                                pass
                if btn_special.clicked(pos) and player_local.special_charge == 100:
                    player_local.attack(enemy_local, special=True)
                    turno_jogador = False
                    esperando = True
                    delay = pygame.time.get_ticks()

        if esperando and pygame.time.get_ticks() - delay > 700:
            esperando = False
            if not enemy_local.dead and not turno_jogador:
                enemy_local.attack(player_local)
            turno_jogador = True

        if enemy_local.dead:
            fase_idx += 1
            pygame.mixer.music.stop()
            if fase_idx >= len(Fases_local):
                Util.certo_txt("Você venceu o jogo!")
                Util.pausa(2)
                return
            carregar_fase_local()

        if player_local.dead:
            pygame.mixer.music.stop()
            title_font = pygame.font.SysFont("Arial", 64)
            btn_retry = BattleButton("Tentar Novamente", WIDTH // 2 - 180, HEIGHT // 2 + 20)
            btn_quit = BattleButton("Sair", WIDTH // 2 + 20, HEIGHT // 2 + 20)
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            while True:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        pos = e.pos
                        if btn_retry.clicked(pos):
                            fase_idx = 0
                            carregar_fase_local()
                            break
                        if btn_quit.clicked(pos):
                            pygame.quit()
                            sys.exit()
                try:
                    screen.blit(background_local, (0, 0))
                except Exception:
                    screen.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                title = title_font.render("Game Over", True, (255, 0, 0))
                screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 2 - 120))
                btn_retry.draw(screen)
                btn_quit.draw(screen)
                pygame.display.update()
                clock.tick(60)

        pygame.display.update()
        clock.tick(60)

def main():
    pygame.display.set_caption('Rural Dungeon - Menu')
    clock_main = pygame.time.Clock()

    btn_width, btn_height = 360, 84
    btn_x = (SCREEN_W - btn_width) // 2
    spacing = 28
    start_btn = MenuButton((btn_x, 220, btn_width, btn_height), 'Comecar Jogo', GREEN)
    select_btn = MenuButton((btn_x, 220 + btn_height + spacing, btn_width, btn_height), 'Selecionar Herói', BLUE)
    exit_btn = MenuButton((btn_x, 220 + 2 * (btn_height + spacing), btn_width, btn_height), 'Sair', RED)

    try:
        music_path_menu = os.path.join(os.path.dirname(__file__), 'Sons', 'awesomeness.wav')
        if os.path.exists(music_path_menu):
            pygame.mixer.music.load(music_path_menu)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
    except Exception:
        pass

    state = 'MENU'
    heroi_obj = None

    running = True
    while running:
        clock_main.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if state == 'MENU':
                    if start_btn.is_clicked(pos):
                        state = 'HERO'
                    if select_btn.is_clicked(pos):
                        state = 'SELECT'
                    if exit_btn.is_clicked(pos):
                        running = False

        if state == 'MENU':
            menu_bg = None
            try:
                bg_path = os.path.join(os.path.dirname(__file__), 'Imagens_dialogos', 'e378a975-e5d9-4162-98be-a6693a7d818a.jpg')
                if os.path.exists(bg_path):
                    menu_bg = pygame.image.load(bg_path).convert()
                    menu_bg = pygame.transform.smoothscale(menu_bg, (SCREEN_W, SCREEN_H))
            except Exception:
                menu_bg = None

            if menu_bg:
                screen.blit(menu_bg, (0, 0))
            else:
                screen.fill((30, 30, 50))

            draw_text(screen, 'Rural Dungeon', 56, 320, 80, color=WHITE)
            mx, my = pygame.mouse.get_pos()
            start_btn.draw(screen, mouse_pos=(mx, my))
            select_btn.draw(screen, mouse_pos=(mx, my))
            exit_btn.draw(screen, mouse_pos=(mx, my))
            pygame.display.flip()

        elif state == 'HERO':
            heroi_obj = hero_creation_screen(screen)
            if heroi_obj is None:
                state = 'MENU'
            else:
                save_personagem_file(heroi_obj)
                save_hero_individual(heroi_obj)
                Util.certo_txt(f'Herói {heroi_obj.nome} criado com sucesso!')
                Util.pausa(1)

                try:
                    try:
                        dialogo_pygame.dialogo_terreo()
                    except Exception:
                        pass

                    try:
                        dialogo_pygame.dialogo_intro_cleyton()
                    except Exception:
                        Util.certo_txt('Erro ao iniciar cena de diálogo do Mestre Cleyton. Retornando ao menu.')
                        Util.pausa(1)

                    start_battle_with_heroi(heroi_obj)

                except Exception:
                    Util.certo_txt('Erro ao executar sequência de diálogos/batalha. Retornando ao menu.')
                    Util.pausa(1)

                state = 'MENU'

        elif state == 'SELECT':
            selection = hero_selection_screen(screen)
            if selection is None:
                state = 'MENU'
            else:
                heroi_obj = selection
                save_heroi_to_file(heroi_obj)
                Util.certo_txt(f'Herói {heroi_obj.nome} carregado!')
                Util.pausa(1)
                state = 'MENU'

    pygame.quit()

if __name__ == '__main__':
    main()
