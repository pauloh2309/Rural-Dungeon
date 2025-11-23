from time import sleep
from os import system, name
from colorama import Fore, Style, init

init(autoreset=True)

class Util:

    def limpar_tela():
        system('cls' if name == 'nt' else 'clear')
    
    def pausa(tempo):
        sleep(tempo)

    def reticencias():
        for i in range(0,3):
            print('.', end='') 
            sleep(1)
    def separacao_cabecalho():
        print('=' * 50)
        
    def continuar():
        input(Fore.YELLOW + 'Pressione ENTER para continuar...' + Fore.RESET)