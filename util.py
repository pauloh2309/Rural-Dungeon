from os import system, name
from time import sleep
from colorama import Fore, Back, Style, init


init(autoreset=True)

class Util:
    def limpar_tela():
        system('cls' if name == 'nt' else 'clear')

    def pausa(tempo):
        sleep(tempo)


    def cabecalho(titulo):
        print('\n')
        print('=' * 100)
        print(Fore.BLUE + '{:^100}'.format(titulo) + Fore.RESET)
        print('=' * 100)

    def continuar():
        input(Fore.LIGHTMAGENTA_EX + '\nPressione ENTER para continuar')

    def erro_txt(msg):
        print(Fore.LIGHTRED_EX + '{}'.format(msg))

    def certo_txt(msg):
        print(Fore.LIGHTGREEN_EX + '{}'.format(msg))

    def rpg_dialogo(texto):
        cont = 0
        texto_recortado = texto.split()
        texto_junto = ' '.join(texto_recortado)
        for i in texto:
            print(i, end='')
            Util.pausa(0.05)
        print('\n')