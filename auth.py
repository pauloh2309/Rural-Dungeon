from colorama import Fore, Back, Style, init
from util import Util

usuarios = []

init(autoreset=True)

class Auth:
    def __init__(self):
        pass

    def cadastro(self):
        Util.limpar_tela()
        Util.cabecalho('Cadastro')
        print(Fore.LIGHTYELLOW_EX + 'O cadastro apenas cumpre a função de salvar as suas informações durante a progressão no RPG!')

        print(Fore.LIGHTYELLOW_EX + 'Caso não queira se cadastrar e prosseguir para o jogo base, sinta-se à vontade')

        Util.continuar()
        Util.limpar_tela()

        nome = str(input('Insira o nome (Não precisa ser o nome real): ').strip())
        self.validacao_nome(nome)
        email = str(input('Insira o e-mail (em caso de recuperação de senha): ').strip().lower())
        self.validacao_email(email)
        senha = str(input('Insira a senha: ').strip())
        self.validacao_senha(senha)

        usuarios.append({'nome': nome, 'email': email, 'senha': senha})

    def login(self):
        Util.limpar_tela()
        nome = str(input('Insira o nome: ').strip())
        self.validacao_nome(nome)
        senha = str(input('Insira a senha: ').strip())
        self.validacao_senha(senha)
        for i in usuarios:
            if nome == i['nome'] and senha == i['senha']:
                print(Fore.LIGHTGREEN_EX + 'Login efetuado com sucesso!')
                print('Bem-vindo, {}'.format(nome))
            elif nome == i['nome'] and senha != i['senha'] or nome != i['nome'] and senha == i['senha'] or nome != i['nome'] and senha != i['senha']:
                Util.erro_txt('Nome ou Senha inválidos, tente novamente!')
                Util.continuar()
                return

    def validacao_nome(self, nome):
        if not nome:
            Util.erro_txt('O nome está vazio, adicione um nome!')
            return
        if len(nome) < 6 or len(nome) > 20:
            Util.erro_txt('O nome ou tem menos de 6 caracteres ou ultrapassa a quantidade máxima de 20')
            return
    def validacao_email(self, email):
        if not email:
            Util.erro_txt('O e-mail está vazio, adicione um e-mail!')
            return
        if not (email.endswith('@gmail.com') or email.endswith('@hotmail.com') or email.endswith('@ufrpe.br')):
            Util.erro_txt('O domínio deste e-mail não está cadastrado ou está incorreto, adicione outro com um dos seguintes formatos: @gmail.com; @hotmail.com; @hotmail.com')
            return

    def validacao_senha(self, senha):
        if not senha:
            Util.erro_txt('A senha está vazia, adicione uma senha!')
            return
        if len(senha) < 6 or len(senha) > 20:
            Util.erro_txt('A senha ou tem menos de 6 caracteres ou ultrapassa a quantidade máxima de 20')
            return




auth = Auth()
auth.cadastro()