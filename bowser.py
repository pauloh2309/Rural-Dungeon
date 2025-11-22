from util import Util
import random
from colorama import Fore, Back, Style, init

init(autoreset=True)

bowser_texto = [{'texto_aparição': '''
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
{'texto_sem_evento': '''
Você:
— Estou com tanta fome, felizmente estou perto do Restaurante Universitário.

"Você caminha até a entrada do prédio. O fluxo de pessoas entrando e saindo é intenso."

Você:
— Certo, primeiro o dever, depois o lazer. Preciso garantir minha entrada.

"Ao passar pela porta, você localiza os guichês de venda no canto do saguão."

Você:
— Ali estão eles.

"Você atravessa o saguão e se posiciona em frente à máquina de tickets, pronto para realizar a compra."
'''}
]

opcoes_roleta = [
    {
        "nome": "A Notificação: 'A Bolsa Caiu!'",
        "tipo": "jackpot",
        "texto_bowser": "Bowser: — O quê?! A burocracia falhou a meu favor? Aproveite sua riqueza temporária!",
        "efeito": "Sua carteira encheu de dinheiro!"
    },
    {
        "nome": "O Golpe da Xerox Colorida",
        "tipo": "falência",
        "texto_bowser": "Bowser: — BWAHAHA! Imprimiu o livro todo colorido sem querer? Diga adeus ao seu dinheiro!",
        "efeito": "Você gastou tudo o que tinha na copiadora."
    },
    {
        "nome": "O Milagre do Ponto Extra", 
        "tipo": "benção",
        "texto_bowser": "Bowser: — Grrr... Sorte de principiante. O professor foi com a sua cara.",
        "efeito": "Você se sente invencível (e aprovado)!"
    },
    {
        "nome": "A Praga do Trabalho em Grupo (Sozinho)",
        "tipo": "maldição",
        "texto_bowser": "Bowser: — Excelente! Seus colegas sumiram e o prazo é amanhã. SOFRA!",
        "efeito": "Sua energia vital foi drenada pelo estresse."
    }
]


chance_spawn = random.randint(1, 10)

class Bowser:
    def __init__(self):
        self.dinheiro = 100.00

    def espaco_bowser():
        Util.limpar_tela()
        if chance_spawn != 1:
            Util.rpg_dialogo(bowser_texto[1]['texto_sem_evento'])
        else:
            Util.rpg_dialogo(bowser_texto[0]['texto_aparição'])

    def roleta_bowser():
        Util.limpar_tela()
        Util.rpg_dialogo('Vamos testar sua sorte e ver o que você consegue na minha maravilhosa roleta!')

        print(Fore.LIGHTYELLOW_EX + 'eventos possíveis:')
        print('=' * 70)
        print('\n—'+ Fore.LIGHTCYAN_EX + ' A Notificação: "A Bolsa Caiu!"')
        print('—' + Fore.LIGHTCYAN_EX + ' O Golpe da Xerox Colorida')
        print('—' + Fore.LIGHTCYAN_EX + ' O Milagre do Ponto Extra')
        print('—' + Fore.LIGHTCYAN_EX + ' A Praga do Trabalho em Grupo (sozinho)\n')
        print('=' * 70)
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
            # Código do personagem recebendo dinheiro
            return
        
        elif escolha_roleta['tipo'] == 'falência':
            Util.evento_bowser(escolha_roleta['nome'], escolha_roleta['tipo'], escolha_roleta['efeito'], escolha_roleta['texto_bowser'])
            # Código do personagem perdendo dinheiro
            return
        
        elif escolha_roleta['tipo'] == 'benção':
            Util.evento_bowser(escolha_roleta['nome'], escolha_roleta['tipo'], escolha_roleta['efeito'], escolha_roleta['texto_bowser'])
            # Código do personagem recebendo vitalidade.
            return
        
        else:
            Util.evento_bowser(escolha_roleta['nome'], escolha_roleta['tipo'], escolha_roleta['efeito'], escolha_roleta['texto_bowser'])
            # Código do personagem perdendo energia/estamina.
            return




Bowser.roleta_bowser()


