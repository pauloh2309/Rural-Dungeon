

import json
import pygame
from pygame import Rect
from heroi import Heroi
from util import Util
import dialogo_pygame
import main_battle


SCREEN_W = 1024
SCREEN_H = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
BLUE = (40, 120, 200)

import os


def draw_text(surface, text, size, x, y, color=BLACK):
    font = pygame.font.SysFont(None, size)
    txt = font.render(text, True, color)
    surface.blit(txt, (x, y))


class Button:
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

    def is_hover(self, pos):
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
        'encontrou_bowser': getattr(heroi, 'encontrou_bowser', 0),
        'interactions': getattr(heroi, 'interactions', [])
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_hero_individual(heroi, folder='heroes'):
    """Save each created hero into a separate file so they can be selected later."""
    try:
        os.makedirs(folder, exist_ok=True)
        import time
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
    """Return list of saved hero files (path, metadata).

    Each item: (path, data_dict)
    """
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


def start_game_with_heroi(heroi):
    """Placeholder: integrate with actual game loop later.

    For now: save selected hero into `save_heroi.json` and `save_personagem.json`
    and print a confirmation via Util.
    """
    save_heroi_to_file(heroi)
    save_personagem_file(heroi)
    Util.certo_txt(f'Iniciando jogo com {heroi.nome}...')
    Util.pausa(1)


def hero_creation_screen(screen):
    clock = pygame.time.Clock()

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
        buttons[f'{key}_minus'] = Button((start_x + 300, y, 40, 32), '-')
        buttons[f'{key}_plus'] = Button((start_x + 350, y, 40, 32), '+')

    confirm_btn = Button((700, 600, 180, 50), 'Confirmar', GREEN)
    cancel_btn = Button((880, 600, 100, 50), 'Voltar', RED)

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
        clock.tick(FPS)
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
                        heroi = Heroi(nome=name.strip(), vida=stats['vida'], defesa=stats['defesa'], ataque=stats['ataque'], iniciativa=stats['iniciativa'], dinheiro_inicial=10.5, estamina=stats['estamina'])
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
        pygame.draw.rect(screen, (245,245,245), name_box_rect, border_radius=6)
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
            pygame.draw.rect(screen, (230,230,230), label_rect, border_radius=6)
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
            pygame.draw.rect(screen, (200,200,200), (bar_x, y + 4, bar_w, 24), border_radius=6)
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
            pygame.draw.rect(screen, (245,245,245), (mx + 20, my + 56, modal_w - 40, 40), border_radius=6)
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
    clock = pygame.time.Clock()
    files = list_saved_heroes()
    idx = 0
    offset_y = 140
    running = True
    while running:
        clock.tick(FPS)
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
                            h = Heroi(nome=data.get('nome',''), vida=data.get('vida',1), defesa=data.get('defesa',1), ataque=data.get('ataque',1), iniciativa=data.get('iniciativa',0), dinheiro_inicial=data.get('dinheiro',10.5), estamina=data.get('estamina',1))
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

        back_btn = Button((880, 40, 100, 40), 'Voltar', RED)
        mx,my = pygame.mouse.get_pos()
        back_btn.draw(screen, mouse_pos=(mx,my))

        pygame.display.flip()

    return None


def main():
    pygame.init()
    try:
        pygame.mixer.init()
        music_path = os.path.join(os.path.dirname(__file__), 'Sons', 'awesomeness.wav')
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
    except Exception:
        pass
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Rural Dungeon - Menu')
    clock = pygame.time.Clock()

    btn_width, btn_height = 360, 84
    btn_x = (SCREEN_W - btn_width) // 2
    spacing = 28
    start_btn = Button((btn_x, 220, btn_width, btn_height), 'Comecar Jogo', GREEN)
    select_btn = Button((btn_x, 220 + btn_height + spacing, btn_width, btn_height), 'Selecionar Herói', BLUE)
    exit_btn = Button((btn_x, 220 + 2 * (btn_height + spacing), btn_width, btn_height), 'Sair', RED)

    state = 'MENU'
    heroi_obj = None

    running = True
    while running:
        clock.tick(FPS)
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
                Util.certo_txt(f'Herói {heroi_obj.nome} criado e salvo em save_heroi.json e save_personagem.json')
                Util.pausa(1)
                try:
                    try:
                        dialogo_pygame.dialogo_terreo()
                    except Exception:
                        pass

                    try:
                        dialogo_pygame.dialogo_intro_cleyton()
                    except Exception:
                        Util.certo_txt('Erro ao iniciar cena de diálogo do Mestre Cleyton.')
                        Util.pausa(1)

                    try:
                        dialogo_pygame.dialogo_nivel_1()
                    except Exception:
                        pass

                    res = main_battle.run_battle(start_fase=0)
                    if res == 'victory':
                        try:
                            dialogo_pygame.dialogo_pos_nivel_1()
                        except Exception:
                            pass
                    elif res == 'quit':
                        state = 'MENU'
                        continue

                    try:
                        dialogo_pygame.dialogo_nivel_2()
                    except Exception:
                        pass

                    try:
                        ru_res = dialogo_pygame.ru_choice_scene(heroi_obj)
                    except Exception:
                        ru_res = {'choice': 'next'}

                    res2 = main_battle.run_battle(start_fase=1)
                    if res2 == 'victory':
                        try:
                            dialogo_pygame.dialogo_pos_nivel_2()
                        except Exception:
                            pass
                    elif res2 == 'quit':
                        state = 'MENU'
                        continue

                    try:
                        dialogo_pygame.dialogo_nivel_3()
                    except Exception:
                        pass

                    res3 = main_battle.run_battle(start_fase=2)
                    if res3 == 'victory':
                        try:
                            dialogo_pygame.dialogo_pos_nivel_3()
                        except Exception:
                            pass
                    elif res3 == 'quit':
                        state = 'MENU'
                        continue

                    try:
                        dialogo_pygame.dialogo_nivel_4()
                    except Exception:
                        pass

                    res4 = main_battle.run_battle(start_fase=3)
                    if res4 == 'victory':
                        try:
                            dialogo_pygame.dialogo_conclusao()
                        except Exception:
                            pass
                    state = 'MENU'
                except Exception:
                    Util.certo_txt('Erro ao executar sequência de diálogos e batalhas. Retornando ao menu.')
                    Util.pausa(1)
                state = 'MENU'

        elif state == 'SELECT':
            selection = hero_selection_screen(screen)
            if selection is None:
                state = 'MENU'
            else:
                save_personagem_file(selection)
                save_hero_individual(selection)
                try:
                    try:
                        dialogo_pygame.dialogo_terreo()
                    except Exception:
                        pass

                    try:
                        dialogo_pygame.dialogo_intro_cleyton()
                    except Exception:
                        Util.certo_txt('Erro ao iniciar cena de diálogo do Mestre Cleyton.')
                        Util.pausa(1)

                    try:
                        dialogo_pygame.dialogo_nivel_1()
                    except Exception:
                        pass

                    res = main_battle.run_battle(start_fase=0)
                    if res == 'victory':
                        try:
                            dialogo_pygame.dialogo_pos_nivel_1()
                        except Exception:
                            pass
                    elif res == 'quit':
                        state = 'MENU'
                        continue

                    try:
                        dialogo_pygame.dialogo_nivel_2()
                    except Exception:
                        pass

                    try:
                        ru_res = dialogo_pygame.ru_choice_scene(selection)
                    except Exception:
                        ru_res = {'choice': 'next'}

                    res2 = main_battle.run_battle(start_fase=1)
                    if res2 == 'victory':
                        try:
                            dialogo_pygame.dialogo_pos_nivel_2()
                        except Exception:
                            pass
                    elif res2 == 'quit':
                        state = 'MENU'
                        continue

                    try:
                        dialogo_pygame.dialogo_nivel_3()
                    except Exception:
                        pass

                    res3 = main_battle.run_battle(start_fase=2)
                    if res3 == 'victory':
                        try:
                            dialogo_pygame.dialogo_pos_nivel_3()
                        except Exception:
                            pass
                    elif res3 == 'quit':
                        state = 'MENU'
                        continue

                    try:
                        dialogo_pygame.dialogo_nivel_4()
                    except Exception:
                        pass

                    res4 = main_battle.run_battle(start_fase=3)
                    if res4 == 'victory':
                        try:
                            dialogo_pygame.dialogo_conclusao()
                        except Exception:
                            pass
                except Exception:
                    Util.certo_txt('Erro ao executar sequência de diálogos e batalhas. Retornando ao menu.')
                    Util.pausa(1)
                state = 'MENU'

    pygame.quit()


if __name__ == '__main__':
    main()
