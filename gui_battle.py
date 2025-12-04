import pygame
import sys
import os
from pygame.locals import *


from game_assets import BOSSES_DATA 

class MockPersonagem:
    def __init__(self, nome, vida, ataque, defesa, estamina, carga=0):
        self.nome = nome
        self.vida = vida
        self.vidabase = vida
        self.ataque = ataque
        self.ataquebase = ataque
        self.defesa = defesa
        self.defesabase = defesa
        self.estamina = estamina
        self.estaminabase = estamina
        self.carga_especial = carga
        self.carga_max_especial = 100
        self.trufa = [{'nome': 'Trufa de morango', 'qnt': 3}]

class MockBatalha:
    usadas_em_batalha = {}
    def atacar_leve(self, atacante, defensor):
        dano = atacante.ataque * 0.8
        defensor.vida = max(0, defensor.vida - int(dano))
        return defensor.vida
    def atacar_pesado(self, atacante, defensor):
        if atacante.estamina < 3: return defensor.vida
        atacante.estamina -= 3
        dano = atacante.ataque * 1.5
        defensor.vida = max(0, defensor.vida - int(dano))
        return defensor.vida
    def atacar_especial(self, atacante, defensor):
        if atacante.carga_especial < atacante.carga_max_especial: return defensor.vida
        dano = atacante.ataque * 2.5
        defensor.vida = max(0, defensor.vida - int(dano))
        return defensor.vida
    def defender(self, personagem):
        personagem.defesa += 10 
    def recuperar_estamina(self, personagem):
        personagem.estamina = min(personagem.estaminabase, personagem.estamina + 2)
    def usar_trufa(self, personagem):
        personagem.vida = min(personagem.vidabase, personagem.vida + 30)
        
Heroi = MockPersonagem
Personagem = MockPersonagem
Batalha = MockBatalha


pygame.init()

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
VERDE = (0, 150, 0)
AZUL = (0, 0, 200)
CINZA_ESCURO = (40, 40, 40)
AMARELO = (255, 255, 0)

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Rural Dungeon Battle")

FONTE = pygame.font.Font(None, 24)
FONTE_MED = pygame.font.Font(None, 30)
FONTE_GRANDE = pygame.font.Font(None, 40)



def desenhar_texto(surface, text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(text_surface, rect)

def desenhar_barra_status(surface, x, y, width, height, current, maximum, color_fill, label):
    pygame.draw.rect(surface, CINZA_ESCURO, (x, y, width, height))
    
    fill_ratio = current / maximum if maximum > 0 else 0
    fill_width = int(width * fill_ratio)
    pygame.draw.rect(surface, color_fill, (x, y, fill_width, height))
    
    pygame.draw.rect(surface, PRETO, (x, y, width, height), 2)
    
    desenhar_texto(surface, label, FONTE, BRANCO, x + 5, y + 5)
    desenhar_texto(surface, f"{current}/{maximum}", FONTE, BRANCO, x + width - 5, y + 5, center=True)


class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.color = AZUL
        self.hover_color = (80, 80, 255)

    def draw(self, surface):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        desenhar_texto(surface, self.text, FONTE_MED, BRANCO, self.rect.centerx, self.rect.centery, center=True)

    def is_clicked(self, event):
        return event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)



class BattleScene:
    def __init__(self, player, boss_key):
        
        boss_data = BOSSES_DATA.get(boss_key)
        if not boss_data:
            raise ValueError(f"Dados do chefe '{boss_key}' não encontrados.")
            
        self.player = player
        self.enemy = Personagem(
            boss_data['nome'],
            *boss_data['stats'] 
        )
        self.batalha_logic = Batalha() 

        self.state = 'DIALOGUE'
        self.current_dialogue = boss_data['dialogue']
        self.dialogue_index = 0
        self.log_messages = [] 
        self.load_assets(boss_data)
        self.setup_ui()

    def load_assets(self, data):
        try:
            self.background = pygame.image.load(data["bg_image"]).convert_alpha()
        except:
            print(f"ATENÇÃO: Não foi possível carregar a imagem de fundo: {data['bg_image']}. Usando fundo preto.")
            self.background = pygame.Surface((LARGURA, ALTURA))
            self.background.fill((0, 0, 0))
            
        self.background = pygame.transform.scale(self.background, (LARGURA, ALTURA))

        try:
            self.sprite_player = pygame.image.load(data["sprite_hero"]).convert_alpha()
            self.sprite_enemy = pygame.image.load(data["sprite_enemy"]).convert_alpha()
            self.sprite_player = pygame.transform.scale(self.sprite_player, (150, 200)) # Ajuste o tamanho
            self.sprite_enemy = pygame.transform.scale(self.sprite_enemy, (200, 250))   # Ajuste o tamanho
        except Exception as e:
            print(f"ATENÇÃO: Falha ao carregar sprites. Usando placeholder. Erro: {e}")
            self.sprite_player = pygame.Surface((150, 200), SRCALPHA)
            self.sprite_player.fill(AZUL)
            self.sprite_enemy = pygame.Surface((200, 250), SRCALPHA)
            self.sprite_enemy.fill(VERMELHO) 


    def setup_ui(self):
        w, h = 180, 40
        x_start, y_start = 590, LARGURA - 170 
        padding = 10
        
        self.action_buttons = [
            Button(x_start, y_start, w, h, "1. Ataque Leve", 'atacar_leve'),
            Button(x_start, y_start + h + padding, w, h, "2. Ataque Pesado (3 EST)", 'atacar_pesado'),
            Button(x_start, y_start + 2*h + 2*padding, w, h, "3. Especial (100 CARGA)", 'atacar_especial'),
            Button(x_start, y_start + 3*h + 3*padding, w, h, "4. Defender", 'defender'),
            Button(x_start, y_start + 4*h + 4*padding, w, h, "5. Recuperar EST", 'recuperar_estamina'),
            Button(x_start, y_start + 5*h + 5*padding, w, h, "6. Usar Trufa", 'usar_trufa'),
        ]
        
    def handle_input(self, event):
        if self.state == 'DIALOGUE':
            if event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE):
                self.dialogue_index += 1
                if self.dialogue_index >= len(self.current_dialogue):
                    self.state = 'PLAYER_TURN'
                return

        elif self.state == 'PLAYER_TURN':
            for button in self.action_buttons:
                if button.is_clicked(event):
                    action_method = getattr(self.batalha_logic, button.action)
                    
                    self.log_messages = []
                    
                    
                    if 'atacar' in button.action:
                        action_method(self.player, self.enemy)
                    elif button.action == 'defender':
                        action_method(self.player)
                    elif button.action == 'recuperar_estamina':
                        action_method(self.player)
                    elif button.action == 'usar_trufa':
                        action_method(self.player)
                        
                    self.state = 'ENEMY_TURN'
                    return

    def update(self):
        if self.state == 'ENEMY_TURN':
            
            if self.enemy.vida <= 0:
                self.state = 'BATTLE_END'
                self.log_messages.append(f"{self.player.nome} Venceu!")
                return
            
            pygame.time.wait(1000) 
            
            self.log_messages.append(f"{self.enemy.nome} atacou...")
            self.batalha_logic.atacar_leve(self.enemy, self.player) 
            
            if self.player.vida <= 0:
                self.state = 'BATTLE_END'
                self.log_messages.append(f"{self.enemy.nome} Venceu! Derrota...")
                return
            
            self.state = 'PLAYER_TURN'
            
    
    def draw(self, surface):
        
        surface.blit(self.background, (0, 0))
        
        surface.blit(self.sprite_player, (100, ALTURA - self.sprite_player.get_height() - 50))
        surface.blit(self.sprite_enemy, (LARGURA - self.sprite_enemy.get_width() - 100, ALTURA - self.sprite_enemy.get_height() - 150))
        
        x_p, y_p, w_p, h_p = 50, ALTURA - 100, 200, 20
        desenhar_barra_status(surface, x_p, y_p, w_p, h_p, self.player.vida, self.player.vidabase, VERDE, "VIDA")
        desenhar_barra_status(surface, x_p, y_p + 25, w_p, h_p, self.player.estamina, self.player.estaminabase, AMARELO, "EST")
        desenhar_barra_status(surface, x_p, y_p + 50, w_p, h_p, self.player.carga_especial, self.player.carga_max_especial, AZUL, "CARGA")
        desenhar_texto(surface, self.player.nome, FONTE_MED, BRANCO, x_p, y_p - 25)

        x_e, y_e, w_e, h_e = LARGURA - 250, 50, 200, 20
        desenhar_barra_status(surface, x_e, y_e, w_e, h_e, self.enemy.vida, self.enemy.vidabase, VERMELHO, "VIDA")
        desenhar_barra_status(surface, x_e, y_e + 25, w_e, h_e, self.enemy.estamina, self.enemy.estaminabase, AMARELO, "EST")
        desenhar_texto(surface, self.enemy.nome, FONTE_MED, BRANCO, x_e, y_e - 25)

        dialogue_box_rect = pygame.Rect(50, LARGURA - 200, 500, 150)
        pygame.draw.rect(surface, CINZA_ESCURO, dialogue_box_rect, border_radius=10)
        pygame.draw.rect(surface, BRANCO, dialogue_box_rect, 2, border_radius=10)
        
        text_x, text_y = dialogue_box_rect.x + 10, dialogue_box_rect.y + 10
        
        if self.state == 'DIALOGUE':
            if self.dialogue_index < len(self.current_dialogue):
                line = self.current_dialogue[self.dialogue_index]
                speaker = line['speaker']
                text = line['text']
                desenhar_texto(surface, f"{speaker}:", FONTE_MED, AMARELO, text_x, text_y)
                
                words = text.split(' ')
                line_to_draw = ""
                y_offset = 0
                for word in words:
                    temp_line = line_to_draw + word + " "
                    if FONTE.size(temp_line)[0] < dialogue_box_rect.width - 20:
                        line_to_draw = temp_line
                    else:
                        desenhar_texto(surface, line_to_draw, FONTE, BRANCO, text_x, text_y + FONTE_MED.get_height() + 5 + y_offset)
                        line_to_draw = word + " "
                        y_offset += FONTE.get_height() + 5
                
                desenhar_texto(surface, line_to_draw, FONTE, BRANCO, text_x, text_y + FONTE_MED.get_height() + 5 + y_offset)
                
        else:
            for i, msg in enumerate(self.log_messages[-3:]):
                desenhar_texto(surface, msg, FONTE_MED, BRANCO, text_x, text_y + i * 25)
            
            if self.state == 'PLAYER_TURN':
                desenhar_texto(surface, "Sua vez. Escolha uma ação:", FONTE_MED, AMARELO, text_x, dialogue_box_rect.bottom - 30)

        if self.state == 'PLAYER_TURN':
            for button in self.action_buttons:
                button.draw(surface)
        elif self.state == 'BATTLE_END':
            overlay = pygame.Surface((LARGURA, ALTURA), SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            
            message = self.log_messages[-1]
            color = VERDE if 'Venceu' in message else VERMELHO
            desenhar_texto(surface, message, FONTE_GRANDE, color, LARGURA // 2, ALTURA // 2, center=True)
            desenhar_texto(surface, "Pressione ESPAÇO para continuar...", FONTE_MED, BRANCO, LARGURA // 2, ALTURA // 2 + 50, center=True)



def main_game_loop():
    player = Heroi(nome="Aluno", vida=120, ataque=25, defesa=10, estamina=5, carga=0)
    
    try:
        current_scene = BattleScene(player, "Administracao") 
    except Exception as e:
        print(f"Erro ao inicializar a cena de batalha: {e}")
        return

    clock = pygame.time.Clock()
    rodando = True
    
    while rodando:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if current_scene:
                current_scene.handle_input(event)

        if current_scene:
            current_scene.update()

        if current_scene:
            current_scene.draw(TELA)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main_game_loop()