import random
from batalha import Batalha
from util import Util
import personagem
from colorama import Fore, Style

class Combate:
    
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.batalha = Batalha()
        self.p = personagem
        self.defesa_aprimorada_p1 = False
        self.defesa_aprimorada_p2 = False
        self.bonus_defesa = 20

    def dados_idimigo(self):
        if self.p2.carga_especial >= self.p2.carga_max_especial:
            return 4 
        return random.choice([1, 1, 1, 2, 2, 3, 5, 5, 5]) 

    def combate_pratico(self):
            turno = 1
            
            while self.p1.vida > 0 and self.p2.vida > 0:
                
                if self.defesa_aprimorada_p1:
                    self.p1.defesa -= self.bonus_defesa
                    self.defesa_aprimorada_p1 = False
                    
                if self.defesa_aprimorada_p2:
                    self.p2.defesa -= self.bonus_defesa
                    self.defesa_aprimorada_p2 = False

                print(f'\n===== TURNO {turno} =====')
                
                print(Fore.GREEN + f'{self.p1.nome}: Vida {self.p1.vida}/{self.p1.vidabase}, Ataque {self.p1.ataque}, Defesa {self.p1.defesa}, Estamina {self.p1.estamina}/{self.p1.estaminabase}, Carga Especial {self.p1.carga_especial}/{self.p1.carga_max_especial}' + Fore.RESET)
                print(Fore.RED + f'{self.p2.nome}: Vida {self.p2.vida}/{self.p2.vidabase}, Ataque {self.p2.ataque}, Defesa {self.p2.defesa}, Estamina {self.p2.estamina}/{self.p2.estaminabase}, Carga Especial {self.p2.carga_especial}/{self.p2.carga_max_especial}' + Fore.RESET)
                Util.separacao_cabecalho()
                
                acao_p1 = 0
                
                while acao_p1 == 0:
                    print('Escolha o número desejado:')
                    print(Fore.CYAN + '1 - Atacar' + Fore.RESET)
                    print(Fore.BLUE + f'2 - Se Defender (Recupera 2 Estamina, +{self.bonus_defesa} Defesa neste turno)' + Fore.RESET)
                    print(Fore.MAGENTA + '3 - Usar Trufa' + Fore.RESET)
                    print('0 - Limpar Tela (ver status novamente)')
                    
                    try:
                        numero1 = int(input("Escolha o numero: ")) 
                    except ValueError:
                        numero1 = -1

                    if numero1 == 0:
                        Util.limpar_tela()
                        continue

                    elif numero1 == 1:
                        sub_numero = 0
                        while sub_numero == 0:
                            Util.limpar_tela()
                            print('Escolha o tipo de ataque:')
                            print(Fore.CYAN + '1 - Ataque Basico (0 Estamina, +15 Carga)' + Fore.RESET)
                            print(Fore.YELLOW + '2 - Ataque Leve (2 Estamina, +25 Carga)' + Fore.RESET)
                            print(Fore.RED + '3 - Ataque Pesado (3 Estamina, +35 Carga)' + Fore.RESET)
                            
                            if self.p1.carga_especial >= self.p1.carga_max_especial:
                                print(Fore.LIGHTRED_EX + '4 - Ataque Especial (Disponível!)' + Fore.RESET)
                            else:
                                print(Fore.BLACK + '4 - Ataque Especial (Carregue: {}/{})'.format(self.p1.carga_especial, self.p1.carga_max_especial) + Fore.RESET)

                            print('5 - Voltar')
                            
                            try:
                                sub_numero = int(input("Escolha o numero: "))
                            except ValueError:
                                sub_numero = -1

                            if sub_numero in [1, 2, 3]:
                                acao_p1 = sub_numero 
                                break
                            elif sub_numero == 4:
                                if self.p1.carga_especial == self.p1.carga_max_especial:
                                    acao_p1 = 4 
                                    break
                                else:
                                    print(Fore.RED + 'Ataque Especial nao esta carregado! Escolha outra acao.' + Fore.RESET)
                                    Util.pausa(2)
                                    break
                            elif sub_numero == 5:
                                Util.limpar_tela()
                                break
                            else:
                                print('Opcao invalida.')
                                Util.pausa(1)
                                sub_numero = 0
                        
                    elif numero1 == 2:
                        acao_p1 = 5
                    elif numero1 == 3:
                        acao_p1 = 6
                    else:
                        print('Opcao invalida.')
                        Util.pausa(1)
                
                acao_p2 = self.dados_idimigo()

                ordem_acao = []
                
                if self.p1.iniciativa > self.p2.iniciativa:
                    ordem_acao = [self.p1, self.p2]
                elif self.p2.iniciativa > self.p1.iniciativa:
                    ordem_acao = [self.p2, self.p1]
                else:
                    if random.choice([True, False]):
                         ordem_acao = [self.p1, self.p2]
                    else:
                         ordem_acao = [self.p2, self.p1]
                         
                
                if acao_p1 == 5:
                    self.p1.defesa += self.bonus_defesa
                    self.defesa_aprimorada_p1 = True
                    
                if acao_p2 == 5:
                    self.p2.defesa += self.bonus_defesa
                    self.defesa_aprimorada_p2 = True

                Util.limpar_tela()
                print(f'\n===== TURNO {turno} =====')
                print(Fore.GREEN + f'{self.p1.nome}: Vida {self.p1.vida}/{self.p1.vidabase}, Ataque {self.p1.ataque}, **Defesa {self.p1.defesa}**, Estamina {self.p1.estamina}/{self.p1.estaminabase}, Carga Especial {self.p1.carga_especial}/{self.p1.carga_max_especial}' + Fore.RESET)
                print(Fore.RED + f'{self.p2.nome}: Vida {self.p2.vida}/{self.p2.vidabase}, Ataque {self.p2.ataque}, **Defesa {self.p2.defesa}**, Estamina {self.p2.estamina}/{self.p2.estaminabase}, Carga Especial {self.p2.carga_especial}/{self.p2.carga_max_especial}' + Fore.RESET)
                Util.separacao_cabecalho()
                
                for personagem_atual in ordem_acao:
                    
                    if self.p1.vida <= 0 or self.p2.vida <= 0:
                        break
                        
                    if personagem_atual == self.p1:
                        acao = acao_p1
                        atacante = self.p1
                        defensor = self.p2
                        acao_defensor = acao_p2 
                    else:
                        acao = acao_p2
                        atacante = self.p2
                        defensor = self.p1
                        acao_defensor = acao_p1 
                        

                    defensor_defendeu = (acao_defensor == 5)

                    
                    if acao == 1:
                        self.batalha.atacar_basico(atacante, defensor, defensor_defendeu)
                    elif acao == 2:
                        self.batalha.atacar_leve(atacante, defensor, defensor_defendeu)
                    elif acao == 3:
                        self.batalha.atacar_pesado(atacante, defensor, defensor_defendeu)
                    
                    elif acao == 4:
                        if atacante.carga_especial == atacante.carga_max_especial:
                            self.batalha.atacar_especial(atacante, defensor, defensor_defendeu)
                        else:
                            if atacante == self.p2:
                                print(Fore.RED + f'{atacante.nome} tentou usar Ataque Especial, mas falhou. Usando ataque Básico.' + Fore.RESET)
                                self.batalha.atacar_basico(atacante, defensor, defensor_defendeu)
                            else:
                                print(Fore.RED + 'Ação inválida: Ataque Especial não carregado. O jogador se defende (por segurança).' + Fore.RESET)
                                acao = 5 

                    if acao == 5:
                        print(Fore.BLUE + f'{atacante.nome} defende e recupera 2 de estamina! (Defesa aprimorada neste turno)' + Fore.RESET)
                        atacante.estamina = min(atacante.estaminabase, atacante.estamina + 2)
                        Util.pausa(2)
                        
                    elif acao == 6 and atacante == self.p1:
                        self.batalha.usar_trufa(atacante)
                
                if self.p1.vida <= 0:
                    if self.defesa_aprimorada_p1: self.p1.defesa -= self.bonus_defesa
                    if self.defesa_aprimorada_p2: self.p2.defesa -= self.bonus_defesa
                    
                    self.batalha.repurar_estatos_posbatalha(self.p2)
                    Util.limpar_tela()
                    print(Fore.RED + '{:^50}'.format(f'FIM DA LUTA! {self.p2.nome} VENCEU') + Fore.RESET)
                    return False
                    
                elif self.p2.vida <= 0:
                    if self.defesa_aprimorada_p1: self.p1.defesa -= self.bonus_defesa
                    if self.defesa_aprimorada_p2: self.p2.defesa -= self.bonus_defesa
                    
                    self.batalha.repurar_estatos_posbatalha(self.p1)
                    Util.limpar_tela()
                    print(Fore.GREEN + '{:^50}'.format(f'FIM DA LUTA! {self.p1.nome} VENCEU') + Fore.RESET)
                    return True
                    
                turno += 1
                self.batalha.repurar_estatos_posbatalha(self.p1)
                self.batalha.repurar_estatos_posbatalha(self.p2)
                Util.limpar_tela()