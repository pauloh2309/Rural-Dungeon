import random
from util import Util
from colorama import Fore, Style, init

init(autoreset=True)

class Batalha:
    usadas_em_batalha = {'Trufa de limão': False, 'Trufa de maracujá': False, 'Trufa de chocolate': False, 'Trufa de café': False, 'Trufa de Hortelã': False, 'Trufa de Coco': False}

    def __init__(self):
        pass

    def calcular_reducao_ativa(self, defensor):
        """Calcula a redução de dano aleatória APENAS se o personagem escolheu defender."""
        chance = random.randint(1, 100)
        
        if chance <= 20:
            print(Fore.BLUE + f'{defensor.nome} se defendeu totalmente! Dano reduzido em 100%.' + Fore.RESET)
            return 1.0 
        elif chance <= 50:
            print(Fore.CYAN + f'{defensor.nome} se defendeu parcialmente! Dano reduzido em 50%.' + Fore.RESET)
            return 0.5 
        else:
            return 0.0 

    def calcular_dano_sorte(self, atacante, base_multiplicador, normal_min_multi, normal_max_multi):
        sorte_roll = random.randint(1, 100)
        dano_base = atacante.ataque * base_multiplicador
        multiplicador_sorte = 1.0
        mensagem_sorte = ''

        CRIT_CHANCE = 5 
        FAIL_CHANCE = 5 

        if sorte_roll <= CRIT_CHANCE: 
            multiplicador_sorte = 2.0
            mensagem_sorte = Fore.YELLOW + 'ACERTO CRÍTICO! (Dano x2.0)' + Fore.RESET
        elif sorte_roll >= (100 - FAIL_CHANCE): 
            multiplicador_sorte = 0.1
            mensagem_sorte = Fore.RED + 'FALHA CRÍTICA! (Dano x0.1)' + Fore.RESET
        else:
            multiplicador_sorte = random.uniform(normal_min_multi, normal_max_multi)
            mensagem_sorte = Fore.WHITE + f'Dano normal com variação (x{multiplicador_sorte:.2f})' + Fore.RESET
        
        dano_bruto = int(dano_base * multiplicador_sorte)
        dano_bruto = max(1, dano_bruto)
        
        print(mensagem_sorte)

        return dano_bruto

    def adicionar_carga_especial(self, atacante, valor):
        if atacante.carga_especial < atacante.carga_max_especial:
            atacante.carga_especial += valor
            atacante.carga_especial = min(atacante.carga_especial, atacante.carga_max_especial)
            print(Fore.MAGENTA + f'{atacante.nome} ganhou {valor} de Carga Especial! ({atacante.carga_especial}/{atacante.carga_max_especial})' + Fore.RESET)

    def aplicar_dano(self, atacante, defensor, dano_bruto, defensor_defendeu=False):
        reducao_dano = 0.0
        
        if defensor_defendeu:
            reducao_dano = self.calcular_reducao_ativa(defensor)
        elif dano_bruto > 0:
            print(Fore.YELLOW + f'{defensor.nome} nao estava defendendo ativamente. Sem chance de mitigacao aleatoria.' + Fore.RESET)

        dano_final = int(dano_bruto * (1.0 - reducao_dano))
        dano_final = max(1, dano_final) if dano_bruto > 0 and dano_final == 0 else max(0, dano_final)
        
        defensor.vida -= dano_final
        defensor.vida = max(0, defensor.vida)
        
        print(f'{atacante.nome} causou {dano_final} de dano em {defensor.nome}!')
        print(f'{defensor.nome} agora tem {defensor.vida} de vida. (Estamina de {atacante.nome}: {atacante.estamina})')
        Util.pausa(2)
        return defensor.vida

    def atacar_basico(self, atacante, defensor, defensor_defendeu=False):
        dano_bruto = self.calcular_dano_sorte(atacante, 0.3, 0.9, 1.1)
        self.adicionar_carga_especial(atacante, 15)
        
        print(f'{atacante.nome} desfere um ataque basico...')
        return self.aplicar_dano(atacante, defensor, dano_bruto, defensor_defendeu)

    def atacar_leve(self, atacante, defensor, defensor_defendeu=False):
        if atacante.estamina < 2:
            print(Fore.RED + f'{atacante.nome} nao tem estamina suficiente para Ataque Leve (requer 2)!' + Fore.RESET)
            Util.pausa(2)
            return defensor.vida
        
        atacante.estamina -= 2
        
        dano_bruto = self.calcular_dano_sorte(atacante, 0.8, 0.8, 1.2)
        self.adicionar_carga_especial(atacante, 25)
        
        print(Fore.YELLOW + f'{atacante.nome} desfere um ataque leve...' + Fore.RESET)
        return self.aplicar_dano(atacante, defensor, dano_bruto, defensor_defendeu)

    def atacar_pesado(self, atacante, defensor, defensor_defendeu=False):
        if atacante.estamina < 3:
            print(Fore.RED + f'{atacante.nome} está muito cansado e não tem estamina para o ataque pesado (requer 3)!' + Fore.RESET)
            Util.pausa(2)
            return defensor.vida

        atacante.estamina -= 3
        
        dano_bruto = self.calcular_dano_sorte(atacante, 1.2, 0.7, 1.3)
        self.adicionar_carga_especial(atacante, 35)

        print(Fore.RED + f'{atacante.nome} executa um ataque PESADO...' + Fore.RESET)
        return self.aplicar_dano(atacante, defensor, dano_bruto, defensor_defendeu)

    def atacar_especial(self, atacante, defensor, defensor_defendeu=False):
        if atacante.carga_especial < atacante.carga_max_especial:
            print(Fore.RED + f'{atacante.nome} nao tem Carga Especial completa ({atacante.carga_especial}/{atacante.carga_max_especial})!' + Fore.RESET)
            Util.pausa(2)
            return defensor.vida

        atacante.carga_especial = atacante.carga_especial - atacante.carga_max_especial
        
        multiplicador_dano_especial = 3 
        dano_base = atacante.ataque * multiplicador_dano_especial
        
        multiplicador_sorte = random.uniform(1.8, 2.2) 
        dano_bruto = int(dano_base * multiplicador_sorte)
        
        print(Fore.LIGHTRED_EX + f'{atacante.nome} executa o ATAQUE ESPECIAL! (Dano x{multiplicador_sorte:.2f})' + Fore.RESET)
        
        return self.aplicar_dano(atacante, defensor, dano_bruto, defensor_defendeu)
    
    def ambos_defende(self):
        print('Ambos os personagens defendem e recuperam 2 de estamina!')
        Util.pausa(2)
        
    def usar_trufa(self, personagem):
        nome_trufa = ''
        opcoes_trufas = {}
        
        for i, trufa in enumerate(personagem.trufa):
            if trufa['qnt'] > 0:
                opcoes_trufas[str(i + 1)] = trufa['nome']
                print(f"{i + 1} - {trufa['nome']} (x{trufa['qnt']}): {trufa['descrição']}")
        
        if not opcoes_trufas:
            print(Fore.RED + "Voce nao tem trufas disponiveis para usar!" + Fore.RESET)
            Util.pausa(2)
            return personagem.vida

        escolha = input("Escolha o numero da trufa que deseja usar (ou ENTER para cancelar): ")
        
        if not escolha:
            return personagem.vida
            
        if escolha in opcoes_trufas:
            nome_trufa = opcoes_trufas[escolha]
            trufa_escolhida = next((t for t in personagem.trufa if t['nome'] == nome_trufa), None)
            
            if trufa_escolhida and trufa_escolhida['qnt'] > 0:
                trufa_escolhida['qnt'] -= 1
                
                if nome_trufa == 'Trufa de morango':
                    cura = 30
                    personagem.vida = min(personagem.vidabase, personagem.vida + cura)
                    print(Fore.GREEN + f'{personagem.nome} usou {nome_trufa} e restaurou {cura} de vida! Vida atual: {personagem.vida}.' + Fore.RESET)
                
                elif nome_trufa == 'Trufa de limão' and not Batalha.usadas_em_batalha[nome_trufa]:
                    personagem.defesa += 20
                    Batalha.usadas_em_batalha[nome_trufa] = True
                    print(Fore.MAGENTA + f'Aumentou a defesa em 20! Defesa atual: {personagem.defesa}.' + Fore.RESET)
                
                elif nome_trufa == 'Trufa de maracujá' and not Batalha.usadas_em_batalha[nome_trufa]:
                    personagem.ataque += 30
                    Batalha.usadas_em_batalha[nome_trufa] = True
                    print(Fore.MAGENTA + f'Aumentou o ataque em 30! Ataque atual: {personagem.ataque}.' + Fore.RESET)

                elif nome_trufa == 'Trufa de chocolate' and not Batalha.usadas_em_batalha[nome_trufa]:
                    personagem.defesa += 10
                    Batalha.usadas_em_batalha[nome_trufa] = True
                    print(Fore.MAGENTA + f'Aumentou a defesa em 10! Defesa atual: {personagem.defesa}.' + Fore.RESET)

                elif nome_trufa == 'Trufa de café' and not Batalha.usadas_em_batalha[nome_trufa]:
                    personagem.ataque += 15
                    Batalha.usadas_em_batalha[nome_trufa] = True
                    print(Fore.MAGENTA + f'Aumentou o ataque em 15! Ataque atual: {personagem.ataque}.' + Fore.RESET)

                elif nome_trufa == 'Trufa de Hortelã' and not Batalha.usadas_em_batalha[nome_trufa]:
                    personagem.defesa += 50
                    Batalha.usadas_em_batalha[nome_trufa] = True
                    print(Fore.MAGENTA + f'Aumentou a defesa em 50! Defesa atual: {personagem.defesa}.' + Fore.RESET)
                
                elif nome_trufa == 'Trufa de Coco' and not Batalha.usadas_em_batalha[nome_trufa]:
                    personagem.ataque += 45
                    Batalha.usadas_em_batalha[nome_trufa] = True
                    print(Fore.MAGENTA + f'Aumentou o ataque em 45! Ataque atual: {personagem.ataque}.' + Fore.RESET)
                
                else:
                    print(Fore.RED + f'Você ja usou uma {nome_trufa} nesta luta!' + Fore.RESET)
                    trufa_escolhida['qnt'] += 1
            
            else:
                print(Fore.RED + 'Opção de trufa invalida.' + Fore.RESET)
                if trufa_escolhida:
                     trufa_escolhida['qnt'] += 1
                
        else:
            print(Fore.RED + f'Escolha invalida.' + Fore.RESET)
            
        Util.pausa(2)
        return personagem.vida

    def recuperar_estatos_completo(self, personagem):
            personagem.vida = personagem.vidabase
            personagem.ataque = personagem.ataquebase
            personagem.defesa = personagem.defesabase
            personagem.estamina = personagem.estaminabase
            personagem.carga_especial = 0
            Batalha.usadas_em_batalha = {'Trufa de limão': False, 'Trufa de maracujá': False, 'Trufa de chocolate': False, 'Trufa de café': False, 'Trufa de Hortelã': False, 'Trufa de Coco': False}
            return personagem.defesa, personagem.ataque, personagem.vida, personagem.estamina
    
    def repurar_estatos_posbatalha(self, personagem):
            personagem.ataque = personagem.ataquebase
            personagem.defesa = personagem.defesabase
            personagem.estamina = min(personagem.estaminabase, personagem.estamina)
            return personagem.defesa, personagem.ataque, personagem.estamina