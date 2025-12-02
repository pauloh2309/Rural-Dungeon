import os
import pygame as pg

if not pg.mixer:
    print('Alerta, o som está desabilitado')
if not pg.font:
    print('Alerta, a fonte está desabilitada')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

pg.init()

def jogo():
    while True:
        tela = (700, 700)
        pg.display.set_mode(tela)
        pg.display.set_caption('RURAL DUNGEON')

jogo()