from util import Util

preco_trufa = 1.50
preco_ru = 3.50

class Personagem:
    def __init__(self, nome, curso):
        self.nome = nome
        self.curso = curso
        self.dinheiro = 10.50
        self.inventario = [
        {'nome': 'Trufa de morango', 'qnt': 3, 'descrição': 'Restaura 30 pontos de saúde.'},
        {'nome': 'Trufa de limão', 'qnt': 3, 'descrição': 'Aumenta a defesa em 20 até o final da luta (só pode ser usado uma vez durante a luta).'},
        {'nome': 'Trufa de maracujá', 'qnt': 3, 'descrição': 'Aumenta o ataque em 30 até o final da luta (só pode ser usado uma vez durante a luta)'},
        ]
    
    def pagar_ru(self):
        if self.dinheiro >= preco_ru:
            self.dinheiro -= preco_ru
            return True
        else:
            return False
    
    def comprar_trufa(self, trufa):
        if self.dinheiro >= preco_trufa:
            self.dinheiro -= preco_trufa
            self.adicionar_item(trufa)
            return True
        else:
            return False
        
    def ganhar(self, valor):
        self.dinheiro += valor

    def adicionar_item(self, nome_item):
        for item in self.inventario:
            if item['nome'] == nome_item:
                item['qnt'] += 1
                return
        
        Util.erro_txt('Este item não existe!')