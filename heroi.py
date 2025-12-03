from personagem1 import Personagem
from colorama import Fore, Style, init
from util import Util

init(autoreset=True)

class Heroi(Personagem):

    def __init__(self, nome='', vida=1, defesa=1, ataque=1, iniciativa=0, dinheiro_inicial=10.5, estamina=1, econtrou_bowser=0, xp = 0, xp_max = 100, nivel = 1):
        super().__init__(nome, vida, defesa, ataque, iniciativa, dinheiro_inicial, estamina, econtrou_bowser)
        self.xp = xp
        self.xp_max = xp_max
        self.nivel = nivel
        self.nivel_atual = 


    def personalizacao(self):
        while True:
            Util.limpar_tela()
            print('Cuidado! Agora você definirá os seguintes status:')
            Util.separacao_cabecalho()
            print(Fore.GREEN + '{:^50}'.format('Força (Ataque)') + Fore.BLUE + '\n{:^50}'.format('Defesa') + Fore.RED + '\n{:^50}'.format('Vida Base') + Fore.CYAN + '\n{:^50}'.format('Iniciativa') + Fore.YELLOW + '\n{:^50}'.format('estamina'))
            Util.separacao_cabecalho()
            print('Total de pontos de status: ' + Fore.YELLOW + '120' + Fore.RESET)
            print('Status Mínimo: 1 ponto por atributo.')
            
            try:
                ataque = int(input('\nPontos em Força (Ataque): '))
                defesa = int(input('Pontos em Defesa: '))
                vida = int(input('Pontos em Vida: '))
                iniciativa = int(input('Pontos em Iniciativa: ')) 
                estamina = int(input('Pontos de estamina: '))
            except ValueError:
                Util.erro_txt('Erro: Adicione apenas números positivos inteiros!')
                Util.pausa(3)
                continue
            
            soma_status = ataque + defesa + vida + iniciativa + estamina
            
            if soma_status > 120:
                Util.erro_txt(f'Seus pontos de status totais superam o limite permitido (120)! Você usou {soma_status} pontos.')
                Util.pausa(3)
            elif soma_status < 120:
                Util.erro_txt(f'Seus pontos de status totais estão abaixo do limite permitido (120)! Você usou {soma_status} pontos.')
                Util.pausa(3)
            elif ataque < 1 or defesa < 1 or vida < 1 or iniciativa < 1 or estamina < 1:
                Util.erro_txt('Cada status deve conter, no mínimo, 1 ponto!')
                Util.pausa(3)
            else:
                self.nome = str(input(Style.BRIGHT + 'Insira o nome do seu herói: ' + Style.NORMAL).strip().capitalize())
                self.ataque = ataque
                self.defesa = defesa
                self.vida = vida
                self.iniciativa = iniciativa
                self.vidabase = vida
                self.ataquebase = ataque
                self.defesabase = defesa
                self.estamina = estamina
                self.estaminabase = estamina

                
                print(Fore.GREEN + f'\nHerói {self.nome} criado com sucesso!' + Fore.RESET)
                Util.pausa(2)
                break
    def ganho_xp(self, quantidade):
        self.xp += quantidade
        if self.xp >= self.xp_max:
            self.nivel += 1
            self.xp -= self.xp_max
            self.xp_max = int(self.xp_max * 1.25)

    def pontos_nivel(self):

