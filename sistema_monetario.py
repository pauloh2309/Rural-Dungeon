from util import Util
from colorama import Fore, Back, Style, init
from random import randint
from personagem import Personagem, preco_ru
from bowser import Bowser

init(autoreset=True)

jogador = {
'dinheiro': 10.50,
'inventario': [
    {'nome': 'Trufa de morango', 'qnt': '3', 'descrição': 'Restaura 30 pontos de saúde.'},
    {'nome': 'Trufa de limão', 'qnt': '3', 'descrição': 'Aumenta a defesa em 20 até o final da luta (só pode ser usado uma vez durante a luta).'},
    {'nome': 'Trufa de maracujá', 'qnt': '3', 'descrição': 'Aumenta o ataque em 30 até o final da luta (só pode ser usado uma vez durante a luta)'},
    ]
}

texto_ru = {'texto_chegando_ru': '''
"Faminto(a), pensando em algum lugar para recarregar as energias...
"Você, então, toma a decisão de ir ao Restaurante Universitário, situado proóximo à Reitoria."


Recepcionista:
— Olá, estudante, seja bem-vindo(a) ao Restaurante Universitário da UFRPE!
— A refeição custa R$ 3,50 e só aceitamos dinheiro físico, você tem dinheiro suficiente?

Você:
— Só um segundo, vou inspecionar minha carteira...
'''
, 'texto_sem_evento': '''
Você:\r\n— Estou com tanta fome, felizmente estou perto do Restaurante Universitário.\r\n\r\n"Você caminha até a entrada do prédio. O fluxo de pessoas entrando e saindo é intenso."\r\n\r\nVocê:\r\n— Puxa, esqueci o dinheiro em casa. Voltar andando pra casa com essa fome...
'''
}
texto_comidas = [
    {'prato': '''
"O prato de hoje é: Arroz, feijão, frango assado e purê de batata."
Você:\r\n— Que delícia, isso vai me dar um gás!\r\n\r\n"Você devora o prato e sente suas energias se renovarem. Você sai do RU pronto para a próxima aventura."
'''},
    {'prato': '''
"O prato de hoje é: Arroz, feijão, carne de porco e macarrão."
Você:\r\n— Nada mal, a comida está quentinha.\r\n\r\n"Você termina a refeição e se sente revigorado, pronto para enfrentar os desafios."
'''},
    {'prato': '''
"O prato de hoje é: Arroz, feijão, bife e salada de alface."
Você:\r\n— Nossa, que dia de sorte! Um bife suculento!\r\n\r\n"Após comer, sua barriga está cheia e sua mente está clara. Você está pronto para o que vier."
'''}]

prato_aleatorio = texto_comidas[randint(0, 2)]['prato']

def restaurante_univ(heroi):
    Util.limpar_tela()
    jogador_dinheiro = heroi.dinheiro 
    Util.rpg_dialogo(texto_ru['texto_chegando_ru'])
    Util.continuar()
    Util.limpar_tela()
    print(Fore.LIGHTYELLOW_EX + 'Você tem R$ {:.2f}.'.format(jogador_dinheiro))
    
    
    if jogador_dinheiro < preco_ru:
        Util.erro_txt('Você não tem dinheiro suficiente, vá trabalhar, seu vagabundo!')
        if heroi.econtrou_bowser == 0:
            bowser_event = Bowser(heroi)
            bowser_event.rola_roleta(bowser_event.bowser_texto[0]['aparição'])
            heroi.econtrou_bowser = 1 
        else:
             Util.rpg_dialogo(texto_ru['texto_sem_evento'])
        return 
    
    else:
        Util.certo_txt('Você tem dinheiro suficiente, não está liso!')
        comer = str(input('\nDeseja comprar o ticket para comer? (s/n)\n').strip().lower())
        if not comer.isalpha():
            Util.erro_txt('Está precisando de um óculos, não aceitamos números!')
            return 
        if comer == 's':
            Util.limpar_tela()
            
            heroi.vida = heroi.vidabase
            heroi.estamina = heroi.estaminabase
            Util.certo_txt(f'Você comprou o ticket e está pronto para almoçar! Vida ({heroi.vida}/{heroi.vidabase}) e Estamina ({heroi.estamina}/{heroi.estaminabase}) restauradas ao máximo!')
            
            heroi.pagar_ru()
            
            Util.rpg_dialogo(prato_aleatorio)
            
            if heroi.econtrou_bowser == 1:
                bowser_event = Bowser(heroi)
                bowser_event.rola_roleta(bowser_event.bowser_texto[1]['re-aparição'])
            
        elif comer == 'n':
            Util.limpar_tela()
            print(Fore.LIGHTCYAN_EX + 'Sério? Você percorreu todo esse caminho... ' + Fore.RESET)
            Util.pausa(2)
        else:
            Util.erro_txt('Opção inválida, voltando ao menu.')
            Util.pausa(2)
        return