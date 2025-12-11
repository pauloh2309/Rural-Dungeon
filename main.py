

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
    if not os.path.isabs(path):
        path = os.path.join(BASE_DIR, path)
    data = {
        'nome': heroi.nome,
        'vida': heroi.vida,
        'defesa': heroi.defesa,
        'ataque': heroi.ataque,
        'dinheiro': getattr(heroi, 'dinheiro', 0),
        'nivel': getattr(heroi, 'nivel', 1),
        'xp': getattr(heroi, 'xp', 0)
    }
    try:
        data['character'] = getattr(heroi, 'character', 'miguel')
    except Exception:
        data['character'] = 'miguel'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_personagem_file(heroi, path='save_personagem.json'):
    if not os.path.isabs(path):
        path = os.path.join(BASE_DIR, path)
    data = {
        'nome': heroi.nome,
        'vida': heroi.vida,
        'defesa': heroi.defesa,
        'ataque': heroi.ataque,
        'dinheiro': getattr(heroi, 'dinheiro', 10.5),
        'encontrou_bowser': getattr(heroi, 'encontrou_bowser', 0),
        'interactions': getattr(heroi, 'interactions', [])
    }
    try:
        data['character'] = getattr(heroi, 'character', 'miguel')
    except Exception:
        data['character'] = 'miguel'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_hero_individual(heroi, folder='heroes'):
    if not os.path.isabs(folder):
        folder = os.path.join(BASE_DIR, folder)

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
            'dinheiro': getattr(heroi, 'dinheiro', 10.5),
            'nivel': getattr(heroi, 'nivel', 1),
            'xp': getattr(heroi, 'xp', 0)
        }
        try:
            data['character'] = getattr(heroi, 'character', 'miguel')
        except Exception:
            data['character'] = 'miguel'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path
    except Exception:
        return None


def save_all_hero_files(heroi):
    try:
        save_heroi_to_file(heroi)
        save_personagem_file(heroi)
        saved_path = save_hero_individual(heroi)
        return saved_path is not None
    except Exception:
        return False


def play_menu_music():
    try:
        music_path = os.path.join(os.path.dirname(__file__), 'Sons', 'awesomeness.wav')
        if os.path.exists(music_path):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
    except Exception:
        pass


def list_saved_heroes(folder='heroes'):

    if not os.path.isabs(folder):
        folder = os.path.join(BASE_DIR, folder)

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
        'vida': 1
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

                        heroi = Heroi(nome=name.strip(), vida=stats['vida'], defesa=stats['defesa'], ataque=stats['ataque'], dinheiro_inicial=10.5)
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
        draw_text(screen, 'Criação de Herói', 60, 370, 40, color=WHITE)

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


def character_select_screen(screen):
    clock = pygame.time.Clock()

    def load_idle_frame(character_folder):
        try:
            base = os.path.join(os.path.dirname(__file__), 'FramesAnimacoes', character_folder, 'idle')
            if not os.path.exists(base):
                base = os.path.join(os.path.dirname(__file__), 'FramesAnimacoes', character_folder)
            if not os.path.exists(base):
                return None

            def sort_key(fname):
                name = os.path.splitext(fname)[0]
                try:
                    return int(name)
                except Exception:
                    return name.lower()

            files = [f for f in os.listdir(base) if os.path.isfile(os.path.join(base, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not files:
                return None
            files = sorted(files, key=sort_key)
            fpath = os.path.join(base, files[0])
            try:
                img = pygame.image.load(fpath).convert_alpha()
                return img
            except Exception:
                return None
        except Exception:
            return None


    mig_pref = os.path.join(os.path.dirname(__file__), 'imagens_game', 'miguel_sembg.png')
    mar_pref = os.path.join(os.path.dirname(__file__), 'imagens_game', 'Personagem_maria.png')

    mig_img = None
    mar_img = None
    try:
        if os.path.exists(mig_pref):
            mig_img = pygame.image.load(mig_pref).convert_alpha()
    except Exception:
        mig_img = None
    try:
        if os.path.exists(mar_pref):
            mar_img = pygame.image.load(mar_pref).convert_alpha()
    except Exception:
        mar_img = None

    if not mig_img:
        mig_img = load_idle_frame('miguel_oco')
    if not mar_img:
        mar_img = load_idle_frame('maria_oco')

    box_w, box_h = 260, 320
    img_w = box_w - 20
    img_h = box_h - 80
    mw = SCREEN_W
    mh = SCREEN_H
    btn_miguel = Rect((mw // 2 - box_w - 20, mh // 2 - box_h // 2, box_w, box_h))
    btn_maria = Rect((mw // 2 + 20, mh // 2 - box_h // 2, box_w, box_h))

    def scale_to_fit(img, target_w, target_h):
        try:
            w, h = img.get_width(), img.get_height()
            if w == 0 or h == 0:
                return None
            scale = min(target_w / w, target_h / h)
            nw = max(1, int(w * scale))
            nh = max(1, int(h * scale))
            return pygame.transform.smoothscale(img, (nw, nh))
        except Exception:
            return None

    if mig_img:
        mig_img = scale_to_fit(mig_img, img_w, img_h)
    if mar_img:
        mar_img = scale_to_fit(mar_img, img_w, img_h)

    font = pygame.font.SysFont(None, 28)

    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pos = e.pos
                if btn_miguel.collidepoint(pos):
                    return 'miguel'
                if btn_maria.collidepoint(pos):
                    return 'maria'

        try:
            bg_path = os.path.join(os.path.dirname(__file__), 'Imagens_dialogos', 'e378a975-e5d9-4162-98be-a6693a7d818a.jpg')
            if os.path.exists(bg_path):
                bg = pygame.image.load(bg_path).convert()
                bg = pygame.transform.smoothscale(bg, (SCREEN_W, SCREEN_H))
                screen.blit(bg, (0, 0))
            else:
                screen.fill((30, 30, 50))
        except Exception:
            screen.fill((30, 30, 50))

        draw_text(screen, 'Escolha o seu personagem', 70, SCREEN_W // 2 - 310, 120, color=WHITE)

        pygame.draw.rect(screen, (70, 70, 70), btn_miguel, border_radius=8)
        if mig_img:
            screen.blit(mig_img, (btn_miguel.x + 10, btn_miguel.y + 10))
        txt = font.render('Masculino', True, WHITE)
        screen.blit(txt, (btn_miguel.x + (btn_miguel.width - txt.get_width()) // 2, btn_miguel.y + btn_miguel.height - 40))

        pygame.draw.rect(screen, (70, 70, 70), btn_maria, border_radius=8)
        if mar_img:
            screen.blit(mar_img, (btn_maria.x + 10, btn_maria.y + 10))
        txt2 = font.render('Feminino', True, WHITE)
        screen.blit(txt2, (btn_maria.x + (btn_maria.width - txt2.get_width()) // 2, btn_maria.y + btn_maria.height - 40))

        pygame.display.flip()



def hero_selection_screen(screen):

    clock = pygame.time.Clock()
    all_files = list_saved_heroes()
    all_files.reverse()
    scroll_offset = 0
    item_height = 84
    items_per_screen = 6
    max_scroll = max(0, len(all_files) - items_per_screen)
    
    delete_confirm = None
    delete_timer = 0
    
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    scroll_offset = max(0, scroll_offset - 1)
                else:
                    scroll_offset = min(max_scroll, scroll_offset + 1)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                
                if delete_confirm is not None:
                    if Rect(300, 400, 200, 50).collidepoint(pos):
                        try:
                            os.remove(delete_confirm[0])
                            all_files = list_saved_heroes()
                            all_files.reverse()
                            max_scroll = max(0, len(all_files) - items_per_screen)
                            scroll_offset = min(scroll_offset, max_scroll)
                            delete_confirm = None
                        except Exception:
                            delete_confirm = None
                    elif Rect(520, 400, 200, 50).collidepoint(pos):
                        delete_confirm = None
                else:
                    for i in range(items_per_screen):
                        idx = scroll_offset + i
                        if idx >= len(all_files):
                            break
                        path, data = all_files[idx]
                        y = 140 + i * item_height
                        box = Rect(60, y, SCREEN_W - 180, 72)
                        delete_btn = Rect(SCREEN_W - 100, y + 6, 90, 60)
                        
                        if delete_btn.collidepoint(pos):
                            delete_confirm = (path, data)
                            break
                        elif box.collidepoint(pos):
                            try:
                                h = Heroi(nome=data.get('nome',''), vida=data.get('vida',1), defesa=data.get('defesa',1), ataque=data.get('ataque',1), iniciativa=data.get('iniciativa',0), dinheiro_inicial=data.get('dinheiro',10.5), estamina=data.get('estamina',1))
                                try:
                                    setattr(h, 'character', data.get('character', 'miguel'))
                                except Exception:
                                    pass
                                return h
                            except Exception:
                                continue
                    
                    if Rect(880, 40, 100, 40).collidepoint(pos):
                        return None

        
        screen.fill((18,18,30))
        
        draw_text(screen, 'Selecione um Heroi', 60, 300, 50, color=WHITE)

        for i in range(items_per_screen):
            idx = scroll_offset + i
            if idx >= len(all_files):
                break
            path, data = all_files[idx]
            y = 140 + i * item_height
            box = Rect(60, y, SCREEN_W - 180, 72)
            delete_btn = Rect(SCREEN_W - 100, y + 6, 90, 60)
            
            pygame.draw.rect(screen, (40,40,60), box, border_radius=8)
            draw_text(screen, data.get('nome','?'), 28, box.x + 12, box.y + 8, color=WHITE)
            info = f"Vida: {data.get('vida',1)}  Ataque: {data.get('ataque',1)}  Defesa: {data.get('defesa',1)}"
            draw_text(screen, info, 20, box.x + 12, box.y + 38, color=(200,200,200))
            
            pygame.draw.rect(screen, RED, delete_btn, border_radius=6)
            delete_text = pygame.font.SysFont(None, 20).render('Deletar', True, WHITE)
            screen.blit(delete_text, (delete_btn.x + 8, delete_btn.y + 18))
        
        if len(all_files) > items_per_screen:
            scroll_pct = scroll_offset / max_scroll if max_scroll > 0 else 0
            scrollbar_y = 140 + scroll_pct * (items_per_screen * item_height - 60)
            pygame.draw.rect(screen, (100,100,100), (SCREEN_W - 20, 140, 10, items_per_screen * item_height))
            pygame.draw.rect(screen, (255,255,255), (SCREEN_W - 20, scrollbar_y, 10, 60))

        back_btn = Button((880, 40, 100, 40), 'Voltar', RED)
        mx,my = pygame.mouse.get_pos()
        back_btn.draw(screen, mouse_pos=(mx,my))
        
        if delete_confirm is not None:
            modal_w = 520
            modal_h = 150
            mx = (SCREEN_W - modal_w) // 2
            my = (SCREEN_H - modal_h) // 2
            modal = pygame.Surface((modal_w, modal_h), flags=pygame.SRCALPHA)
            modal.fill((10, 10, 10, 220))
            screen.blit(modal, (mx, my))
            
            confirm_text = f"Deletar {delete_confirm[1].get('nome', '?')}?"
            draw_text(screen, confirm_text, 28, mx + 40, my + 20, color=WHITE)
            
            btn_yes = Rect(300, 400, 200, 50)
            btn_no = Rect(520, 400, 200, 50)
            
            pygame.draw.rect(screen, (200, 50, 50), btn_yes, border_radius=6)
            pygame.draw.rect(screen, (50, 50, 200), btn_no, border_radius=6)
            
            draw_text(screen, 'Sim, Deletar', 22, btn_yes.x + 30, btn_yes.y + 12, color=WHITE)
            draw_text(screen, 'Nao, Voltar', 22, btn_no.x + 35, btn_no.y + 12, color=WHITE)

        pygame.display.flip()

    return None


def run_campaign(heroi_obj):
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

        levels = [
            (0, getattr(dialogo_pygame, 'dialogo_nivel_1', None), getattr(dialogo_pygame, 'dialogo_pos_nivel_1', None)),
            (1, getattr(dialogo_pygame, 'dialogo_nivel_2', None), getattr(dialogo_pygame, 'dialogo_pos_nivel_2', None)),
            (2, getattr(dialogo_pygame, 'dialogo_nivel_3', None), getattr(dialogo_pygame, 'dialogo_pos_nivel_3', None)),
            (3, getattr(dialogo_pygame, 'dialogo_nivel_4', None), getattr(dialogo_pygame, 'dialogo_conclusao', None)),
        ]

        for fase_idx, pre_dialog, post_dialog in levels:
            if callable(pre_dialog):
                try:
                    pre_dialog()
                except Exception:
                    pass

            res = main_battle.run_battle(start_fase=fase_idx, heroi=heroi_obj)

            if res == 'victory':
                if callable(post_dialog):
                    try:
                        post_dialog()
                    except Exception:
                        pass
            elif res == 'quit':
                return 'quit'
    except Exception:
        Util.certo_txt('Erro ao executar sequência de diálogos e batalhas. Retornando ao menu.')
        Util.pausa(1)
        return 'quit'

    return 'done'


def main():
    pygame.init()
    try:
        pygame.mixer.init()
        current_game_volume = load_volume()
        music_path = os.path.join(os.path.dirname(__file__), 'Sons', 'awesomeness.wav')
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(current_game_volume)
            pygame.mixer.music.play(-1)
    except Exception:
        current_game_volume = 0.6
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Rural Dungeon - Menu')
    clock = pygame.time.Clock()

    btn_width, btn_height = 360, 84
    btn_x = (SCREEN_W - btn_width) // 2
    spacing = 28
    start_btn = Button((btn_x, 220, btn_width, btn_height), 'Comecar Jogo', GREEN)
    select_btn = Button((btn_x, 220 + btn_height + spacing, btn_width, btn_height), 'Selecionar Herói', BLUE)
    exit_btn = Button((btn_x, 220 + 2 * (btn_height + spacing), btn_width, btn_height), 'Sair', RED)

    options_btn_size = 64
    options_btn_x = SCREEN_W - options_btn_size - 20
    options_btn_y = 20
    options_btn_rect = Rect((options_btn_x, options_btn_y, options_btn_size, options_btn_size))
    options_img = None
    try:
        options_path = os.path.join(os.path.dirname(__file__), 'imagens_game', 'opção_botão.png')
        if os.path.exists(options_path):
            options_img = pygame.image.load(options_path).convert_alpha()
            options_img = pygame.transform.scale(options_img, (options_btn_size, options_btn_size))
    except Exception:
        pass

    current_volume = load_volume()

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
                
                # Controle de volume em qualquer estado (exceto OPTIONS)
                if state != 'OPTIONS':
                    volume_bar_x = SCREEN_W - 200
                    volume_bar_y = 80
                    volume_bar_width = 150
                    
                    if (volume_bar_x <= pos[0] <= volume_bar_x + volume_bar_width and 
                        volume_bar_y - 10 <= pos[1] <= volume_bar_y + 20):
                        current_volume = (pos[0] - volume_bar_x) / volume_bar_width
                        current_volume = max(0.0, min(1.0, current_volume))
                        pygame.mixer.music.set_volume(current_volume)
                        save_volume(current_volume)
                
                if state == 'MENU':
                    if start_btn.is_clicked(pos):
                        state = 'HERO'
                    if select_btn.is_clicked(pos):
                        state = 'SELECT'
                    if exit_btn.is_clicked(pos):
                        running = False
                    if options_btn_rect.collidepoint(pos):
                        state = 'OPTIONS'
                elif state == 'OPTIONS':
                    volume_bar_left = SCREEN_W // 2 - 150
                    volume_bar_right = SCREEN_W // 2 + 150
                    volume_bar_y = SCREEN_H // 2 + 50
                    
                    if volume_bar_left <= pos[0] <= volume_bar_right and volume_bar_y - 5 <= pos[1] <= volume_bar_y + 5:
                        current_volume = (pos[0] - volume_bar_left) / (volume_bar_right - volume_bar_left)
                        current_volume = max(0.0, min(1.0, current_volume))
                        pygame.mixer.music.set_volume(current_volume)
                        save_volume(current_volume)
                    
                    back_btn_rect = Rect((SCREEN_W // 2 - 80, SCREEN_H - 120, 160, 50))
                    if back_btn_rect.collidepoint(pos):
                        state = 'MENU'
                        save_volume(current_volume)

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

            draw_text(screen, 'Rural Dungeon', 80, 320, 150, color=WHITE)
            mx, my = pygame.mouse.get_pos()
            start_btn.draw(screen, mouse_pos=(mx, my))
            select_btn.draw(screen, mouse_pos=(mx, my))
            exit_btn.draw(screen, mouse_pos=(mx, my))
            
            if options_img:
                if options_btn_rect.collidepoint(mx, my):
                    highlighted = pygame.Surface((options_btn_size, options_btn_size))
                    highlighted.fill((255, 255, 255))
                    highlighted.set_alpha(50)
                    screen.blit(highlighted, (options_btn_x, options_btn_y))
                screen.blit(options_img, (options_btn_x, options_btn_y))
            
            # Desenhar barra de volume no MENU
            volume_bar_x = SCREEN_W - 200
            volume_bar_y = 80
            volume_bar_width = 150
            
            pygame.draw.rect(screen, (50, 50, 50), (volume_bar_x, volume_bar_y, volume_bar_width, 10), border_radius=5)
            fill_width = volume_bar_width * current_volume
            pygame.draw.rect(screen, (100, 255, 100), (volume_bar_x, volume_bar_y, fill_width, 10), border_radius=5)
            
            vol_font = pygame.font.SysFont(None, 16)
            vol_text = vol_font.render(f'{int(current_volume * 100)}%', True, WHITE)
            screen.blit(vol_text, (volume_bar_x - 30, volume_bar_y - 5))
            
            pygame.display.flip()

        elif state == 'OPTIONS':
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

            draw_text(screen, 'Opções', 70, 420, 160, color=WHITE)
            
            volume_label_y = SCREEN_H // 2
            draw_text(screen, 'Volume:', 50, 320, volume_label_y - 40, color=WHITE)
            
            volume_bar_y = SCREEN_H // 2 + 50
            volume_bar_left = SCREEN_W // 2 - 150
            volume_bar_right = SCREEN_W // 2 + 150
            volume_bar_width = volume_bar_right - volume_bar_left
            
            mx, my = pygame.mouse.get_pos()
            
            pygame.draw.rect(screen, (50, 50, 50), (volume_bar_left, volume_bar_y - 5, volume_bar_width, 10), border_radius=5)
            
            fill_width = volume_bar_width * current_volume
            pygame.draw.rect(screen, (100, 255, 100), (volume_bar_left, volume_bar_y - 5, fill_width, 10), border_radius=5)
            
            volume_percent = int(current_volume * 100)
            volume_font = pygame.font.SysFont(None, 28)
            volume_text = volume_font.render(f'{volume_percent}%', True, WHITE)
            volume_text_rect = volume_text.get_rect(center=(SCREEN_W // 2, volume_bar_y + 40))
            screen.blit(volume_text, volume_text_rect)
            
            back_btn_rect = Rect((SCREEN_W // 2 - 80, SCREEN_H - 120, 160, 50))
            back_btn_color = GRAY
            if back_btn_rect.collidepoint(mx, my):
                back_btn_color = tuple(min(255, c + 30) for c in GRAY)
            
            pygame.draw.rect(screen, back_btn_color, back_btn_rect, border_radius=8)
            back_font = pygame.font.SysFont(None, 28)
            back_text = back_font.render('Voltar', True, BLACK)
            back_text_rect = back_text.get_rect(center=back_btn_rect.center)
            screen.blit(back_text, back_text_rect)
            
            pygame.display.flip()

        elif state == 'HERO':
            heroi_obj = hero_creation_screen(screen)
            if heroi_obj is None:
                state = 'MENU'
            else:
                try:
                    choice = character_select_screen(screen)
                    if choice is None:
                        state = 'MENU'
                        continue
                    setattr(heroi_obj, 'character', choice)
                    dialogo_pygame.current_player_name = heroi_obj.nome
                    try:
                        base = os.path.dirname(__file__)
                        if str(choice).lower() == 'maria':
                            dialogo_pygame.current_player_img_path = os.path.join(base, 'imagens_game', 'Personagem_maria.png')
                        else:
                            dialogo_pygame.current_player_img_path = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
                    except Exception:
                        pass
                    if save_all_hero_files(heroi_obj):
                        Util.certo_txt(f'Heroi {heroi_obj.nome} salvo com sucesso em heroes!')
                        Util.pausa(0.5)
                    else:
                        Util.certo_txt('Aviso: erro ao salvar heroi. Continuando...')
                        Util.pausa(0.5)
                except Exception:
                    pass
                res = run_campaign(heroi_obj)
                state = 'MENU'
                play_menu_music()
                if res == 'quit':
                    continue

        elif state == 'SELECT':
            selection = hero_selection_screen(screen)
            if selection is None:
                state = 'MENU'
            else:
                try:
                    choice = character_select_screen(screen)
                    if choice is None:
                        state = 'MENU'
                        continue
                    setattr(selection, 'character', choice)
                    dialogo_pygame.current_player_name = selection.nome
                    try:
                        base = os.path.dirname(__file__)
                        if str(choice).lower() == 'maria':
                            dialogo_pygame.current_player_img_path = os.path.join(base, 'imagens_game', 'Personagem_maria.png')
                        else:
                            dialogo_pygame.current_player_img_path = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
                    except Exception:
                        pass
                    if save_all_hero_files(selection):
                        Util.certo_txt(f'Heroi {selection.nome} atualizado com sucesso!')
                        Util.pausa(0.5)
                    else:
                        Util.certo_txt('Aviso: erro ao salvar heroi. Continuando...')
                        Util.pausa(0.5)
                except Exception:
                    pass
                res = run_campaign(selection)
                state = 'MENU'
                play_menu_music()
                if res == 'quit':
                    continue

    pygame.quit()


if __name__ == '__main__':
    main()
