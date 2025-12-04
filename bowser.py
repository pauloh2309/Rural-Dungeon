from util import Util
import random
from colorama import Fore, Back, Style, init

init(autoreset=True)

class Bowser:
    
    bowser_texto = [
    {'aparição': '''
Você:
— Estou com tanta fome, felizmente estou perto do Restaurante Universitário.

"Você sente sente seu pé esquerdo afundando levemente e, imediatamente, um som estranho"

Você:
— O que é isso?

"O chão desaparece aos seus pés, fazendo-o cair no que parece ser um... cano verde?"
"Você desliza pelo cano e, ao final, cai perante um ser que está virado de costas"

???:
— Vejo que tenho um convidado curioso...

Você:
— Quem é você?

???:
— Eu?... sou o maior pesadelo dos universitários, me chamo Bowser!

Você:
— Bowser? Aquele personagem do Mário? Por que um ser fictício estaria no meu mundo?

Bowser:
— Tem que trabalhar fi, a vida não é um morango.
— Agora, vou girar uma roleta que pode te "enriquecer" ou empobrecer, não você tenha uma boa quantia. Vejamos o que receberá!
'''},
    {'re-aparição': '''
Você:
— Estou com tanta fome, felizmente estou perto do Restaurante Universitário.

"Você sente sente seu pé esquerdo afundando levemente e, imediatamente, um som estranho"

Você:
— O que é isso?

"O chão desaparece aos seus pés, fazendo-o cair no que parece ser um... cano verde?"
"Você desliza pelo cano e, ao final, cai perante um ser que está virado de costas"

Bowser:
— Vejo que nos reencontramos! Não pense que porque pagou seu RU você está livre do meu jogo...
— Gire a roleta novamente, e veremos se você se beneficiará ou se arrependerá de ter me encontrado de novo!
'''}]
    
    
    def __init__(self, heroi):
        self.heroi = heroi

    def rola_roleta(self, texto):
        opcoes_roleta = [
            {'nome': 'Mega-Sena (Ganho de R$ 20.00)', 'tipo': 'jackpot', 'efeito': '+20 Dinheiro', 'texto_bowser': 'Ganho inesperado!'},
            {'nome': 'Aula de Álgebra (Perda de R$ 10.00)', 'tipo': 'falência', 'efeito': '-10 Dinheiro', 'texto_bowser': 'Perdeu, Playboy!'},
            {'nome': 'Aula de Cálculo (Perda de R$ 5.00)', 'tipo': 'falência', 'efeito': '-5 Dinheiro', 'texto_bowser': 'Você tem sorte que não foi pior!'},
            {'nome': 'Recarga de Vitalidade (Aumento de 5 Vida Base)', 'tipo': 'benção', 'efeito': '+5 Vidabase', 'texto_bowser': 'Uma bênção de vitalidade!'},
            {'nome': 'Recarga de Estamina (Aumento de 5 Estamina Base)', 'tipo': 'benção', 'efeito': '+5 Estaminabase', 'texto_bowser': 'Uma bênção de estamina!'},
            {'nome': 'Prova Surpresa (Perda de 50 Vida)', 'tipo': 'maldição', 'efeito': '-50 Vida', 'texto_bowser': 'Isso que dá não estudar!'},
            {'nome': 'Trabalho em Grupo (Perda de 50 Estamina)', 'tipo': 'maldição', 'efeito': '-50 Estamina', 'texto_bowser': 'Trabalho em grupo é sempre um terror!'}
        ]
        
        Util.rpg_dialogo(texto)
        Util.continuar()
        
        escolha_roleta = random.choice(opcoes_roleta)
        Util.limpar_tela()
        print('O dev não se esforçou para fazer uma animação de roleta, então vai ser assim mesmo...')
        print('Girando a roleta...')
        Util.pausa(5)
        Util.limpar_tela()
        print('O resultado é... ' + Fore.YELLOW + '{}.'.format(escolha_roleta['nome']))
        Util.pausa(3)
        Util.limpar_tela()
        
        if escolha_roleta['tipo'] == 'jackpot':
            Util.evento_bowser(escolha_roleta['nome'], escolha_roleta['tipo'], escolha_roleta['efeito'], escolha_roleta['texto_bowser'])
            if escolha_roleta['nome'] == 'Mega-Sena (Ganho de R$ 20.00)':
                self.heroi.dinheiro += 20.00
                print(Fore.GREEN + f'{self.heroi.nome} ganhou R$ 20.00! Dinheiro atual: R$ {self.heroi.dinheiro:.2f}.' + Fore.RESET)
            
            Util.continuar()
            return
        
        elif escolha_roleta['tipo'] == 'falência':
            Util.evento_bowser(escolha_roleta['nome'], escolha_roleta['tipo'], escolha_roleta['efeito'], escolha_roleta['texto_bowser'])
            
            if escolha_roleta['nome'] == 'Aula de Álgebra (Perda de R$ 10.00)':
                perda = min(self.heroi.dinheiro, 10.00)
                self.heroi.dinheiro -= perda
                print(Fore.RED + f'{self.heroi.nome} perdeu R$ {perda:.2f}! Dinheiro atual: R$ {self.heroi.dinheiro:.2f}.' + Fore.RESET)
            elif escolha_roleta['nome'] == 'Aula de Cálculo (Perda de R$ 5.00)':
                perda = min(self.heroi.dinheiro, 5.00)
                self.heroi.dinheiro -= perda
                print(Fore.RED + f'{self.heroi.nome} perdeu R$ {perda:.2f}! Dinheiro atual: R$ {self.heroi.dinheiro:.2f}.' + Fore.RESET)
            
            Util.continuar()
            return
        
        elif escolha_roleta['tipo'] == 'benção':
            Util.evento_bowser(escolha_roleta['nome'], escolha_roleta['tipo'], escolha_roleta['efeito'], escolha_roleta['texto_bowser'])
            
            if escolha_roleta['nome'] == 'Recarga de Vitalidade (Aumento de 5 Vida Base)':
                self.heroi.vidabase += 5
                self.heroi.vida += 5
                print(Fore.GREEN + f'{self.heroi.nome} recebeu uma bênção! Sua Vida Base e atual aumentaram em 5. Nova Vida: {self.heroi.vida}/{self.heroi.vidabase}' + Fore.RESET)
            elif escolha_roleta['nome'] == 'Recarga de Estamina (Aumento de 5 Estamina Base)':
                self.heroi.estaminabase += 5
                self.heroi.estamina += 5
                print(Fore.GREEN + f'{self.heroi.nome} recebeu uma bênção! Sua Estamina Base e atual aumentaram em 5. Nova Estamina: {self.heroi.estamina}/{self.heroi.estaminabase}' + Fore.RESET)
            
            Util.continuar()
            return
        
        else:
            Util.evento_bowser(escolha_roleta['nome'], escolha_roleta['tipo'], escolha_roleta['efeito'], escolha_roleta['texto_bowser'])
            
            if escolha_roleta['nome'] == 'Prova Surpresa (Perda de 50 Vida)':
                perda = 50
                self.heroi.vida = max(0, self.heroi.vida - perda)
                print(Fore.RED + f'{self.heroi.nome} recebeu uma maldição e perdeu {perda} de Vida. Vida atual: {self.heroi.vida}/{self.heroi.vidabase}' + Fore.RESET)
            elif escolha_roleta['nome'] == 'Trabalho em Grupo (Perda de 50 Estamina)':
                perda = 50
                self.heroi.estamina = max(0, self.heroi.estamina - perda)
                print(Fore.RED + f'{self.heroi.nome} recebeu uma maldição e perdeu {perda} de Estamina. Estamina atual: {self.heroi.estamina}/{self.heroi.estaminabase}' + Fore.RESET)
            
            Util.continuar()
            return

    def rola_roleta_gui(self, texto=None):
        """Versão da roleta adaptada para uso em GUI/dialogs.

        Não usa Util para imprimir nem pausar; aplica os efeitos ao `heroi`
        e retorna um dicionário com informações para a interface.
        """
        import random

        opcoes_roleta = [
            {'nome': 'Mega-Sena (Ganho de R$ 20.00)', 'tipo': 'jackpot', 'efeito': '+20 Dinheiro', 'texto_bowser': 'Ganho inesperado!'},
            {'nome': 'Aula de Álgebra (Perda de R$ 10.00)', 'tipo': 'falência', 'efeito': '-10 Dinheiro', 'texto_bowser': 'Perdeu, Playboy!'},
            {'nome': 'Aula de Cálculo (Perda de R$ 5.00)', 'tipo': 'falência', 'efeito': '-5 Dinheiro', 'texto_bowser': 'Você tem sorte que não foi pior!'},
            {'nome': 'Recarga de Vitalidade (Aumento de 5 Vida Base)', 'tipo': 'benção', 'efeito': '+5 Vidabase', 'texto_bowser': 'Uma bênção de vitalidade!'},
            {'nome': 'Recarga de Estamina (Aumento de 5 Estamina Base)', 'tipo': 'benção', 'efeito': '+5 Estaminabase', 'texto_bowser': 'Uma bênção de estamina!'},
            {'nome': 'Prova Surpresa (Perda de 50 Vida)', 'tipo': 'maldição', 'efeito': '-50 Vida', 'texto_bowser': 'Isso que dá não estudar!'},
            {'nome': 'Trabalho em Grupo (Perda de 50 Estamina)', 'tipo': 'maldição', 'efeito': '-50 Estamina', 'texto_bowser': 'Trabalho em grupo é sempre um terror!'}
        ]

        escolha_roleta = random.choice(opcoes_roleta)
        outcome_text = ''

        if escolha_roleta['tipo'] == 'jackpot':
            if escolha_roleta['nome'] == 'Mega-Sena (Ganho de R$ 20.00)':
                self.heroi.dinheiro = getattr(self.heroi, 'dinheiro', 0) + 20.00
                outcome_text = f'{self.heroi.nome} ganhou R$ 20.00! Dinheiro atual: R$ {self.heroi.dinheiro:.2f}.'

        elif escolha_roleta['tipo'] == 'falência':
            if escolha_roleta['nome'] == 'Aula de Álgebra (Perda de R$ 10.00)':
                perda = min(getattr(self.heroi, 'dinheiro', 0), 10.00)
                self.heroi.dinheiro = getattr(self.heroi, 'dinheiro', 0) - perda
                outcome_text = f'{self.heroi.nome} perdeu R$ {perda:.2f}! Dinheiro atual: R$ {self.heroi.dinheiro:.2f}.'
            elif escolha_roleta['nome'] == 'Aula de Cálculo (Perda de R$ 5.00)':
                perda = min(getattr(self.heroi, 'dinheiro', 0), 5.00)
                self.heroi.dinheiro = getattr(self.heroi, 'dinheiro', 0) - perda
                outcome_text = f'{self.heroi.nome} perdeu R$ {perda:.2f}! Dinheiro atual: R$ {self.heroi.dinheiro:.2f}.'

        elif escolha_roleta['tipo'] == 'benção':
            if escolha_roleta['nome'] == 'Recarga de Vitalidade (Aumento de 5 Vida Base)':
                self.heroi.vidabase = getattr(self.heroi, 'vidabase', getattr(self.heroi, 'vida', 0)) + 5
                self.heroi.vida = getattr(self.heroi, 'vida', 0) + 5
                outcome_text = f'{self.heroi.nome} recebeu uma bênção! Vida atual: {self.heroi.vida}/{self.heroi.vidabase}.'
            elif escolha_roleta['nome'] == 'Recarga de Estamina (Aumento de 5 Estamina Base)':
                self.heroi.estaminabase = getattr(self.heroi, 'estaminabase', getattr(self.heroi, 'estamina', 0)) + 5
                self.heroi.estamina = getattr(self.heroi, 'estamina', 0) + 5
                outcome_text = f'{self.heroi.nome} recebeu uma bênção! Estamina atual: {self.heroi.estamina}/{self.heroi.estaminabase}.'

        else:
            if escolha_roleta['nome'] == 'Prova Surpresa (Perda de 50 Vida)':
                perda = 50
                self.heroi.vida = max(0, getattr(self.heroi, 'vida', 0) - perda)
                outcome_text = f'{self.heroi.nome} recebeu uma maldição e perdeu {perda} de Vida. Vida atual: {self.heroi.vida}/{getattr(self.heroi, "vidabase", self.heroi.vida)}.'
            elif escolha_roleta['nome'] == 'Trabalho em Grupo (Perda de 50 Estamina)':
                perda = 50
                self.heroi.estamina = max(0, getattr(self.heroi, 'estamina', 0) - perda)
                outcome_text = f'{self.heroi.nome} recebeu uma maldição e perdeu {perda} de Estamina. Estamina atual: {self.heroi.estamina}/{getattr(self.heroi, "estaminabase", self.heroi.estamina)}.'

        return {
            'escolha': escolha_roleta,
            'outcome_text': outcome_text,
            'texto_bowser': escolha_roleta.get('texto_bowser', '')
        }