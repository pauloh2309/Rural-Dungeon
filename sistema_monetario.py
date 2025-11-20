from util import Util
from colorama import Fore, Back, Style, init
from random import randint
from personagem import Personagem

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
'''}
texto_comidas = [{'prato': '''
Você se dirige ao balcão e recebe o prato do dia: frango grelhado, arroz soltinho e feijão fresquinho.

Você:
— Nossa… isso aqui tá com uma cara maravilhosa!

Ao sentar-se, você começa a comer. O aroma e o sabor do frango bem temperado te animam imediatamente.

Você:
— Era exatamente disso que eu precisava… Sinto até minhas forças voltando.

Conforme termina o prato, uma sensação de energia percorre seu corpo. Você se sente revitalizado(a) e pronto(a) para continuar sua jornada!
'''},
{'prato': '''
Você pega seu prato no balcão: macarrão quentinho coberto com um molho de tomate bem temperado e uma camada generosa de queijo derretido.

Você:
— Olha só isso… até brilha! Hora de recuperar as energias.

A cada garfada, o sabor caseiro do molho parece aquecer seu coração.

Você:
— Ufa… isso revigora qualquer um. Estou me sentindo muito melhor!

Ao terminar a refeição, você respira fundo, sentindo o corpo mais leve e a mente mais desperta. Energia renovada!
'''},
{'prato': '''
No balcão, você recebe um prato leve porém caprichado: alface crocante, tomate, pepino, cenoura ralada e uma colher de grão-de-bico. Acompanhado de um copo de suco natural gelado.

Você:
— Hm… saudável e bonito. Vamos ver se me dá um gás.

Você começa a comer, sentindo a crocância e a leveza da refeição que refresca até a alma.

Você:
— Nossa… até parece que minha vida voltou ao corpo. Que sensação boa!

Quando termina, percebe que o cansaço de antes foi embora. Você se sente renovado(a) e pronto(a) para o que vier!
'''}]

prato_aleatorio = texto_comidas[randint(0, 2)]['prato']

def restaurante_univ():
    Util.limpar_tela()
    jogador_dinheiro = jogador['dinheiro']
    Util.rpg_dialogo(texto_ru['texto_chegando_ru'])
    Util.continuar()
    Util.limpar_tela()
    print(Fore.LIGHTYELLOW_EX + 'Você tem R$ {:.2f}.'.format(jogador_dinheiro))
    if jogador_dinheiro < 3.50:
        Util.erro_txt('Você não tem dinheiro suficiente, vá trabalhar, seu vagabundo!')
        return #Menu!
    
    else:
        Util.certo_txt('Você tem dinheiro suficiente, não está liso!')
        comer = str(input('\nDeseja comprar o ticket para comer? (s/n)\n').strip().lower())
        if not comer.isalpha():
            Util.erro_txt('Está precisando de um óculos, não aceitamos números!')
            return 
        if comer == 's':
            Util.limpar_tela()
            Util.certo_txt('Você comprou o ticket e está pronto para almoçar!')
            jogador_dinheiro -= 3.50
            jogador['dinheiro'] = jogador_dinheiro
        elif comer == 'n':
            Util.limpar_tela()
            print(Fore.LIGHTCYAN_EX + 'Sério? Você percorreu todo esse caminho para sair de mãos abanando?')
            return
        else:
            Util.erro_txt('Escolha apenas entre umas das opções disponibilizadas!')
            return
    Util.rpg_dialogo(prato_aleatorio)

        # Colocar a função do jogador restaurando sua vida

restaurante_univ()
print(jogador['dinheiro'])
