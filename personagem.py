from util import Util

preco_trufa = 1.50
preco_ru = 3.50

class Personagem:
    def __init__(self, nome, vida, defesa, ataque, iniciativa,dinheiro, estamina, econtrou_bowser=0):
        self.nome = nome
        self.defesa = defesa
        self.ataque = ataque
        self.vida = vida
        self.vidabase = vida
        self.ataquebase = ataque
        self.defesabase = defesa
        self.iniciativa = iniciativa
        self.dinheiro = dinheiro
        self.estamina = estamina
        self.estaminabase = estamina
        self.econtrou_bowser = econtrou_bowser

        self.carga_especial = 0
        self.carga_max_especial = 100
        
        self.trufa = [
            {'nome': 'Trufa de morango', 'qnt': 3, 'descrição': 'Restaura 30 pontos de saúde.'},
            {'nome': 'Trufa de limão', 'qnt': 3, 'descrição': 'Aumenta a defesa em 20 até o final da luta (só pode ser usado uma vez durante a luta).'},
            {'nome': 'Trufa de maracujá', 'qnt': 3, 'descrição': 'Aumenta o ataque em 30 até o final da luta (só pode ser usado uma vez durante a luta)'},
            {'nome': 'Trufa de chocolate', 'qnt': 3, 'descrição': 'Aumenta a defesa em 10 até o final da luta (só pode ser usado uma vez durante a luta)'},
            {'nome': 'Trufa de café', 'qnt': 3, 'descrição': 'Aumenta o ataque em 15 até o final da luta (só pode ser usado uma vez durante a luta)'},
            {'nome': 'Trufa de Hortelã', 'qnt': 3, 'descrição': 'Aumenta a defesa em 50 até o final da luta (só pode ser usado uma vez durante a luta)'},
            {'nome': 'Trufa de Coco', 'qnt': 3, 'descrição': 'Aumenta o ataque em 45 até o final da luta (só pode ser usado uma vez durante a luta)'}
        ]


    def ganhar_itens(self):
        for item in self.itens:
            item['qnt'] += 2
            
    def pagar_ru(self):
        if self.dinheiro >= preco_ru:
            self.dinheiro -= preco_ru
            return True
        else:
            return False
    
    def comprar_trufa(self, nome_trufa, valor_trufa):
        if self.dinheiro >= valor_trufa:
            self.dinheiro -= valor_trufa
            for trufa in self.trufa:
                if trufa['nome'] == nome_trufa:
                    trufa['qnt'] += 1
                    return True
        return False