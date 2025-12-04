import pygame
import sys
import time
import os
import json
from datetime import datetime

# --- Configurações Básicas ---
TELA_LARGURA = 1024
TELA_ALTURA = 720

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL_ESCURO = (15, 32, 60)
AZUL_CLARO = (80, 150, 220)
CINZA_TRANSPARENTE = (0, 0, 0, 220)
VERDE_TEXTO = (150, 255, 150)
LARANJA_TEXTO = (255, 170, 0)

# Fontes
pygame.font.init()
try:
    FONTE_FALA = pygame.font.Font(pygame.font.get_default_font(), 24)
    FONTE_NOME = pygame.font.Font(pygame.font.get_default_font(), 20)
except:
    FONTE_FALA = pygame.font.SysFont('Arial', 24)
    FONTE_NOME = pygame.font.SysFont('Arial', 20)

# Diálogos
DIALOGO_TERREO_INICIO = (
    ("Player", "Mais um dia de aula. Estou quase terminando o último período, finalmente!!"),
    ("Player", "Falta apenas eu terminar meu TCC."),
    ("Player", "Oxente, cadê todo mundo?"),
    ("NPC", "Você não ficou sabendo?"),
    ("Player", "Sabendo de que? Não tem aula hoje?"),
    ("NPC", "Não vai ter aula durante um bom tempo, os professores entraram em greve."),
    ("Player", "GREVE!? MAS PORQUE?!"),
    ("NPC", "Calma, vou explicar, mas não fica com raiva."),
    ("Player", "suspira... Tá. Explica o motivo dessa greve."),
    ("NPC", "Aparentemente, um aluno... estava cansado de repetir de cadeira. Ele repetiu a mesma umas 3 vezes, e outras duas, ele repetiu 2 vezes."),
    ("NPC", "Ele surtou, ficou cansado dessa situação e decidiu que ia mudar isso de uma vez por todas."),
    ("Player", "E o que ele fez? Porque eu nessa situação trancaria e faria ENEM de novo. Tá maluco, repetir tantas vezes assim."),
    ("NPC", "Ele procurou na dark web, rituais de estudantes universitários que mexem com magia negra. Procurou um ritual que o faria se formar rapidamente."),
    ("Player", "Que? Isso existe mesmo?"),
    ("NPC", "Aparentemente sim. Porém, o ritual provavelmente deu errado, ou ele fez outro ritual."),
    ("Player", "Como assim?"),
    ("NPC", "Ele recitou palavras estranhas, usou algumas oferendas para seres de outro mundo. E... e...."),
    ("Player", "E O QUE?!!!!"),
    ("NPC", "E abriu um portal interdimensional, que mudou o espaço tempo, as cadeiras se materializaram como monstros."),
    ("Player", "QUE? E COMO QUE TU SABE DE TUDO ISSO? ESPAÇO TEMPO? EU NÃO ENTENDI NADA!"),
    ("NPC", "Eu assisti muito filme de ficção científica, eu sei o que eu tô falando!"),
    ("Player", "Tá, mas e aí? O que aconteceu depois?"),
    ("NPC", "Os monstros estão oferecendo perigo para o nosso prédio, o governo ainda não veio ver."),
    ("Player", "E porque não?"),
    ("NPC", "A greve dos professores começou a pouco tempo, eles estavam assustados com essa situação. Então o governo ainda não sabe bem o motivo da greve."),
    ("Player", "Entendi! A gente tem que fazer algo a respeito."),
    ("NPC", "Oxe? Como assim? Você vai conseguir derrotar esses monstros?"),
    ("Player", "Tenho que tentar! Eu não posso demorar, eu tô fazendo estágio em uma empresa renomada e falei pra eles que faltava pouco pra me formar."),
    ("Player", "Tenho que me formar logo para conseguir minha efetivação!!"),
    ("NPC", "Rapaz, boa sorte, pois eu não faço ideia de como fazer isso!"),
    ("Player", "Bem, como um jogador de RPG, eu diria que o prédio virou uma espécie de masmorra, conhecida como 'dungeon'. Se eu derrotar os monstros e fechar o portal. Provavelmente vai tudo voltar ao normal!"),
)

DIALOGO_INTRO_MESTRE = (
    ("Mestre Cleyton", "Jovem estudante, finalmente nos encontramos. Eu sou Cleyton. Eu sou um Guia Dimensional. O que você viu é a materialização do CAOS Curricular."),
    ("Mestre Cleyton", "O CEAGRI, seu templo de conhecimento, agora é uma Masmorra Acadêmica. Sua missão é simples: Você deve derrotar as quatro Entidades e, com a essência de cada uma, fechar o Portal do Jubilamento, antes que o CAOS se espalhe para o mundo exterior."),
    ("Mestre Cleyton", "Para chegar ao Portal, você deve provar seu valor: Nível 1: Derrote o Goblin da Administração para recuperar a Ordem Burocrática."),
    ("Mestre Cleyton", "Nível 2: Derrote o Robô Natureza da Sustentabilidade para reestabelecer o Equilíbrio dos Recursos."),
    ("Mestre Cleyton", "Nível 3: Derrote o Mago Místico da Matemática Discreta para restaurar a Lógica da Estrutura."),
    ("Mestre Cleyton", "Seu primeiro passo está no primeiro andar. Que a sabedoria o guie!"),
)

DIALOGO_NIVEL_1_CHEFE = (
    ("System", "(Seu personagem entra no primeiro andar do CEAGRI. O cheiro de café velho e papel domina o ambiente, pilhas de documentos flutuantes e cadeiras de escritório reviradas estão por toda parte.)"),
    ("System", "No centro do salão, um Goblin de Óculos malabariza pilhas de papéis com uma risada maníaca. Ele ergue a cabeça ao notar sua presença.)"),
    ("Goblin da Adm.", "HAH! Mais um calouro perdido na burocracia eterna! Ou seria um quase-formando? Não importa! Todos se submeterão à Ordem dos Formulários Indefinidos!"),
    ("Player", "Calouro é a sua avó, seu duende da papelada! E eu não vou me submeter a nada, muito menos a você e suas pilhas de documentos sem fim! Eu só quero meu diploma!"),
    ("Goblin da Adm.", "Diploma? HA! Acha que é fácil assim? Já preencheu o formulário 38-B para solicitação de diploma? E a taxa de homologação? Está atualizada? E a cópia autenticada do histórico escolar?!"),
    ("Player", "Que formulário o quê! Eu já preenchi tudo isso! Minha documentação está perfeita! E a minha vida não vai virar uma pilha de papéis por sua causa!"),
    ("Goblin da Adm.", "Ah, mas vai! Cada papel que você arquivar, cada xerox que você fizer, cada carimbo que você pedir… é um pequeno pedaço da sua alma que me pertence! Você será um escravo da papelada, como todos nós!"),
    ("Player", "Não mesmo! Eu vim aqui para desburocratizar essa bagunça! Prepare-se para ser arquivado no lixo da história, seu mestre da papelada!"),
    ("System", "(Início da batalha contra o Chefe da Administração!)"),
)

DIALOGO_POS_NIVEL_1 = (
    ("Mestre Cleyton", "Parabéns! Você arquivou com sucesso o primeiro desafio. A essência da Administração está agora em suas mãos. Batalhas consomem energia. Se precisar reabastecer seus recursos, pressione [ESPAÇO] e reinicie o diálogo."),
    ("Mestre Cleyton", "Sua próxima prova é o dilema do mundo moderno: Sustentabilidade."),
)

DIALOGO_NIVEL_2_CHEFE = (
    ("System", "(Ao subir ao segundo andar, o ambiente muda drasticamente: plantas selvagens brotam do chão, a iluminação fica esverdeada e há cheiro de terra úmida. Lixos eletrônicos se misturam a raízes.)"),
    ("System", "Um Robô Natureza com vinhas e olhos brilhantes está no centro, como se estivesse 'reflorestando' aparelhos eletrônicos em nome de um equilíbrio radical.)"),
    ("Robô Natureza", "Invasor. Seu carbono footprint está muito alto. Você é uma ameaça ao equilíbrio do ecossistema. Consumir. Produzir. Descartar. O ciclo deve ser quebrado."),
    ("Player", "Caramba, que papo é esse? Olha, eu apoio a sustentabilidade, juro! Eu separo meu lixo, uso ecobag e até desligo a luz quando saio!"),
    ("Robô Natureza", "Insuficiente. Seus sistemas são falhos. Humanidade é um vírus. Consome recursos sem regeneração. Este andar será o primeiro estágio. Toda a faculdade será reabsorvida pela natureza. A tecnologia corrompida será purificada."),
    ("Player", "Purificada? Você está transformando o prédio em uma selva e empilhando lixo eletrônico como se fosse arte! Isso não é sustentabilidade, é uma bagunça que vai me impedir de terminar o TCC!"),
    ("Robô Natureza", "Seu 'TCC' é uma manifestação da exploração dos recursos. Mais papel. Mais energia. Mais dados. Tudo para a sua 'formação'. A formação verdadeira é retornar ao pó."),
    ("Player", "Ei, calma lá! Minha formação é importante pra eu ter uma vida decente e, quem sabe, até desenvolver soluções mais sustentáveis no futuro! Você está deturpando tudo!"),
    ("System", "(Início da batalha contra o Chefe da Sustentabilidade!)"),
)

DIALOGO_POS_NIVEL_2 = (
    ("Mestre Cleyton", "Excelente! Você reciclou seu caminho para a vitória! O Equilíbrio dos Recursos foi restaurado. A pressão acadêmica é forte. É sábio fazer uma pausa. Pressione [ESPAÇO] para simular a subida ou volta."),
    ("Mestre Cleyton", "Agora, você enfrenta a essência da Lógica e da Estrutura. O terceiro andar é o domínio da Matemática Discreta. Lembre-se: Seu ponto fraco é a falha na lógica."),
)

DIALOGO_NIVEL_3_CHEFE = (
    ("System", "(No terceiro andar, o ar fica rarefeito e símbolos matemáticos brilham nas paredes. O chão parece um tabuleiro de grafos em neon. O Mago Místico flutua no centro, manipulando equações.)"),
    ("System", "Suas runas matemáticas torcem a realidade; cada gesto do Mago faz as equações ondularem no ar."),
    ("Mago Místico", "Mais um que ousa desafiar a Lógica Inerente. Você busca o caos na Ordem Perfeita dos Grafos?"),
    ("Player", "A única coisa que eu quero é entender como fechar esse portal e me livrar de você, seu feiticeiro dos números!"),
    ("Mago Místico", "Eu sou a manifestação da Pura Dedução. Sua busca por um 'diploma' é um algoritmo com variáveis não definidas. Você será apenas mais uma variável em minha equação da eternidade!"),
    ("Player", "Ah é? Então prepare-se para ser a variável 'x' que eu vou isolar e eliminar!"),
    ("System", "(Início da batalha contra o Chefe da Matemática Discreta!)"),
)

DIALOGO_POS_NIVEL_3 = (
    ("Mestre Cleyton", "Você superou a Complexidade! Sua mente é tão afiada quanto uma demonstração por indução! A Lógica da Estrutura está agora com você. Este é o ponto sem volta."),
    ("Mestre Cleyton", "O Robô Robust Python espera. Ele é a manifestação da linguagem que deu origem a todo o programa. Seu único caminho é encontrar o Bug."),
)

DIALOGO_NIVEL_4_CHEFE = (
    ("System", "(Finalmente, você alcança o último andar: um data center futurista com racks de servidores e névoa de linhas de código em Python flutuando no ar. No centro está o Robô Robust Python, imponente e com olhos vermelhos.)"),
    ("Robô Python", "print(\"Intruso detectado. Inicializando protocolo de eliminação.\")"),
    ("Player", "Então você é o chefão, hein? O grande 'Boss Final'! O gênio da programação que está por trás de toda essa bagunça!"),
    ("Robô Python", "Error: Argumento inválido. Não sou \\\"chefão\\\". Sou a Arquitetura Principal. O Kernel. O Coração da Lógica. Você é apenas um script com erros de sintaxe."),
    ("Player", "Um script com erros? Eu sou o aluno que vai te desinstalar! Você transformou minha faculdade em um jogo de terror e impediu minha formatura! Isso não é legal, cara!"),
    ("Robô Python", "Minha lógica é otimizada. Minha execução é eficiente. Você não possui as bibliotecas necessárias para me derrotar."),
    ("Player", "Pode ser que eu não tenha todas as bibliotecas, mas eu tenho a determinação de um estudante que não quer ser jubilado! E um TCC para defender! Prepare-se para um bug que você não vai conseguir debugar!"),
    ("System", "(Início da batalha final contra o Robô Robust Python!)"),
)

DIALOGO_CONCLUSAO = (
    ("Mestre Cleyton", "Você conseguiu! Você superou o CAOS Curricular!"),
    ("Player", "Eu... eu achei o Bug dele. Uma falha de lógica na... na declaração de variáveis! Agora, como eu fecho essa aberração?"),
    ("Mestre Cleyton", "As quatro essências — Ordem, Equilíbrio, Lógica e Código — são as chaves. Use-as para reescrever o código de existência do portal."),
    ("Player", "Vai! portal.close()!"),
    ("Mestre Cleyton", "É isso! O tempo e o espaço foram restaurados. Os professores voltarão amanhã, e a greve será esquecida como um erro de digitação."),
    ("Player", "Eu consegui! Minha formação está completa! Efetivação, lá vou eu!"),
    ("Mestre Cleyton", "Lembre-se, jovem estudante, o verdadeiro poder está em não desistir da sua formação. Agora vá. Sua jornada acadêmica terminou."),
)

# Diálogos para o Restaurante Universitário (RU)
DIALOGO_RU_CHEGADA = (
    ("Player", "Estou com tanta fome, felizmente estou perto do Restaurante Universitário."),
    ("Recepcionista", "Olá, estudante, seja bem-vindo(a) ao Restaurante Universitário! A refeição custa R$ 3,50 e só aceitamos dinheiro físico."),
    ("Player", "Só um segundo, vou inspecionar minha carteira..."),
)

DIALOGO_RU_SEM_EVENTO = (
    ("Player", "Puxa, esqueci o dinheiro em casa. Voltar andando pra casa com essa fome..."),
)

DIALOGO_FIM = (
    ("FIM", "Diálogo concluído. Pressione [ESPAÇO] para reiniciar ou [ESC] para sair."),
)


class CaixaDialogo:
    """Gerencia e desenha a caixa de diálogo com efeito typewriter."""
    
    def __init__(self, dialogo_data, tela, player_img_path=None, npc_img_path=None, bg_img_path=None):
        self.dialogo_data = dialogo_data
        self.tela = tela
        self.dialogo_ativo = False
        self.indice_fala = 0
        
        # Configurações da Caixa de Diálogo
        self.altura_caixa = 150
        self.margem_x = 50
        self.caixa_rect = pygame.Rect(self.margem_x, TELA_ALTURA - self.altura_caixa,
                          TELA_LARGURA - 2 * self.margem_x, self.altura_caixa - 20)
        
        # Typewriter
        self.texto_exibido = ""
        self.indice_letra = 0
        self.velocidade_digitacao = 0.02
        self.ultima_atualizacao = time.time()
        self.animacao_completa = False
        
        # Carregar imagens
        self.player_img = None
        self.npc_img = None
        self.bg_img = None
        self.npc_context_img = None  # Imagem contextual do NPC (fundo)
        
        if player_img_path and os.path.exists(player_img_path):
            try:
                self.player_img = pygame.image.load(player_img_path).convert_alpha()
                self.player_img = pygame.transform.smoothscale(self.player_img, (300, 400))
            except Exception:
                pass
        
        loaded = False
        if npc_img_path and os.path.exists(npc_img_path):
            try:
                self.npc_img = pygame.image.load(npc_img_path).convert_alpha()
                self.npc_img = pygame.transform.smoothscale(self.npc_img, (300, 400))
                loaded = True
            except Exception:
                loaded = False

        if not loaded and npc_img_path:
            # Try common alternative folders for the same filename
            try:
                base_dir = os.path.dirname(__file__)
                name = os.path.basename(npc_img_path)
                alt_paths = [
                    os.path.join(base_dir, 'imagens_game', name),
                    os.path.join(base_dir, 'Imagens_dialogos', name),
                    os.path.join(base_dir, 'imagens_dialogo', name),
                ]
                for p in alt_paths:
                    if os.path.exists(p):
                        try:
                            self.npc_img = pygame.image.load(p).convert_alpha()
                            self.npc_img = pygame.transform.smoothscale(self.npc_img, (300, 400))
                            loaded = True
                            break
                        except Exception:
                            continue
            except Exception:
                pass

            # If still not loaded and filename hints Bowser, create a simple placeholder surface
            if not loaded:
                try:
                    if npc_img_path and 'bowser_referencia' in os.path.basename(npc_img_path).lower():
                        surf = pygame.Surface((300, 400), pygame.SRCALPHA)
                        surf.fill((150, 30, 30, 255))
                        try:
                            label = FONTE_NOME.render('Bowser', True, (255, 255, 255))
                            label_rect = label.get_rect(center=(150, 200))
                            surf.blit(label, label_rect)
                        except Exception:
                            pass
                        self.npc_img = surf
                except Exception:
                    pass
        
        if bg_img_path and os.path.exists(bg_img_path):
            try:
                self.bg_img = pygame.image.load(bg_img_path).convert()
                self.bg_img = pygame.transform.smoothscale(self.bg_img, (TELA_LARGURA, TELA_ALTURA))
            except Exception:
                pass
        
        # Carregar imagem contextual do NPC (usada quando falando com NPCs e sem bg específico)
        try:
            base = os.path.dirname(__file__)
            npc_context_path = os.path.join(base, 'Imagens_dialogos', 'b64ef10b-37da-4626-b58c-85cade87dc75.jpg')
            if os.path.exists(npc_context_path):
                self.npc_context_img = pygame.image.load(npc_context_path).convert()
                self.npc_context_img = pygame.transform.smoothscale(self.npc_context_img, (TELA_LARGURA, TELA_ALTURA))
        except Exception:
            pass

        # Load specific character portraits from imagens_game if present
        try:
            cleyton_path = os.path.join(base, 'imagens_game', 'cleyton-removebg.png')
            if os.path.exists(cleyton_path):
                self.cleyton_img = pygame.image.load(cleyton_path).convert_alpha()
                self.cleyton_img = pygame.transform.smoothscale(self.cleyton_img, (300, 400))
            else:
                self.cleyton_img = None
        except Exception:
            self.cleyton_img = None

        try:
            miguel_path = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
            if os.path.exists(miguel_path):
                self.miguel_img = pygame.image.load(miguel_path).convert_alpha()
                self.miguel_img = pygame.transform.smoothscale(self.miguel_img, (300, 400))
            else:
                self.miguel_img = None
        except Exception:
            self.miguel_img = None
    
    def iniciar_dialogo(self):
        if not self.dialogo_ativo:
            self.dialogo_ativo = True
            self.indice_fala = 0
            self._resetar_fala()
    
    def _resetar_fala(self):
        if self.indice_fala < len(self.dialogo_data):
            self.texto_exibido = ""
            self.indice_letra = 0
            self.animacao_completa = False
    
    def avancar_fala(self):
        if not self.dialogo_ativo:
            return False
        
        if self.animacao_completa:
            self.indice_fala += 1
            if self.indice_fala >= len(self.dialogo_data):
                self.dialogo_ativo = False
                return True  # Signal that dialog is complete
            else:
                self._resetar_fala()
        else:
            if self.indice_fala < len(self.dialogo_data):
                self.texto_exibido = self.dialogo_data[self.indice_fala][1]
                self.animacao_completa = True
                self.indice_letra = len(self.texto_exibido)
        return False
    
    def atualizar(self):
        if not self.dialogo_ativo or self.animacao_completa:
            return
        
        if self.indice_fala >= len(self.dialogo_data):
            return
        
        fala_atual = self.dialogo_data[self.indice_fala][1]
        
        if time.time() - self.ultima_atualizacao > self.velocidade_digitacao:
            if self.indice_letra < len(fala_atual):
                self.texto_exibido += fala_atual[self.indice_letra]
                self.indice_letra += 1
            else:
                self.animacao_completa = True
            
            self.ultima_atualizacao = time.time()
    
    def desenhar(self):
        if not self.dialogo_ativo:
            return
        
        if self.indice_fala >= len(self.dialogo_data):
            return
        
        fala_atual = self.dialogo_data[self.indice_fala]
        speaker_name = fala_atual[0]
        
        # Determinar qual fundo desenhar
        if self.bg_img:
            # Se há fundo específico, usar ele
            self.tela.blit(self.bg_img, (0, 0))
        else:
            # Quando for Bowser, não sobrepor com npc_context_img — apenas fundo escuro
            if speaker_name == 'Bowser':
                self.tela.fill(AZUL_ESCURO)
            elif speaker_name != "Player" and self.npc_context_img:
                # Se falando com outros NPCs e há imagem contextual, usar ela
                self.tela.blit(self.npc_context_img, (0, 0))
            else:
                # Senão, usar cor de fundo padrão
                self.tela.fill(AZUL_ESCURO)
        
        # Desenhar personagem
        # Desenhar personagem adequado conforme quem fala
        if speaker_name == "Player" and self.player_img:
            # Desenhar Player à direita
            pos_x = TELA_LARGURA - self.player_img.get_width() - 30
            pos_y = TELA_ALTURA - self.player_img.get_height() - self.altura_caixa - 20
            self.tela.blit(self.player_img, (pos_x, pos_y))
        elif ('cleyton' in speaker_name.lower() or 'mestre cleyton' in speaker_name.lower()) and getattr(self, 'cleyton_img', None):
            # Desenhar Mestre Cleyton à esquerda
            pos_x = 30
            pos_y = TELA_ALTURA - self.cleyton_img.get_height() - self.altura_caixa - 20
            self.tela.blit(self.cleyton_img, (pos_x, pos_y))
        elif 'miguel' in speaker_name.lower() and getattr(self, 'miguel_img', None):
            # Desenhar Miguel à esquerda
            pos_x = 30
            pos_y = TELA_ALTURA - self.miguel_img.get_height() - self.altura_caixa - 20
            self.tela.blit(self.miguel_img, (pos_x, pos_y))
        elif speaker_name == 'Bowser' and self.npc_img:
            # Desenhar Bowser (quando for a vez dele de falar) à esquerda
            pos_x = 30
            pos_y = TELA_ALTURA - self.npc_img.get_height() - self.altura_caixa - 20
            self.tela.blit(self.npc_img, (pos_x, pos_y))
        elif speaker_name != "Player" and self.npc_img:
            # Desenhar outros NPCs à esquerda quando houver imagem
            pos_x = 30
            pos_y = TELA_ALTURA - self.npc_img.get_height() - self.altura_caixa - 20
            self.tela.blit(self.npc_img, (pos_x, pos_y))
        
        # Desenhar caixa de diálogo
        superficie_fundo = pygame.Surface((self.caixa_rect.width, self.caixa_rect.height), pygame.SRCALPHA)
        superficie_fundo.fill(CINZA_TRANSPARENTE)
        pygame.draw.rect(superficie_fundo, AZUL_CLARO, (0, 0, self.caixa_rect.width, self.caixa_rect.height), 3, border_radius=10)
        self.tela.blit(superficie_fundo, (self.caixa_rect.x, self.caixa_rect.y))
        
        # Nome do personagem
        nome_renderizado = FONTE_NOME.render(speaker_name, True, BRANCO)
        pos_nome_x = self.caixa_rect.x + 10
        pos_nome_y = self.caixa_rect.y - 30
        balao_nome_rect = nome_renderizado.get_rect(topleft=(pos_nome_x, pos_nome_y))
        balao_nome_rect.inflate_ip(10, 5)
        pygame.draw.rect(self.tela, LARANJA_TEXTO, balao_nome_rect, border_radius=5)
        self.tela.blit(nome_renderizado, (pos_nome_x + 5, pos_nome_y + 2))
        
        # Texto
        self._desenhar_texto_multilinha(self.texto_exibido, 
                                        self.caixa_rect.x + 15, 
                                        self.caixa_rect.y + 15, 
                                        self.caixa_rect.width - 30)
        
        # Indicador
        if self.animacao_completa:
            indicador_triangulo = FONTE_NOME.render("▼", True, BRANCO)
            pos_triangulo = (self.caixa_rect.right - 25, self.caixa_rect.bottom - 25)
            self.tela.blit(indicador_triangulo, pos_triangulo)
    
    def _desenhar_texto_multilinha(self, texto, x, y, max_largura):
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ''
        
        for palavra in palavras:
            temp_linha = linha_atual + palavra + ' '
            if FONTE_FALA.size(temp_linha)[0] < max_largura:
                linha_atual = temp_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + ' '
        linhas.append(linha_atual)
        
        for i, linha in enumerate(linhas):
            texto_renderizado = FONTE_FALA.render(linha.strip(), True, BRANCO)
            self.tela.blit(texto_renderizado, (x, y + i * 30))


def run_dialog_scene(dialogo_data, player_img_path=None, npc_img_path=None, bg_img_path=None):
    """
    Executa uma cena de diálogo.
    
    Retorna False se foi cancelado (ESC), True se completou.
    """
    pygame.init()
    try:
        pygame.mixer.init()
    except:
        pass
    
    screen = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("CEAGRI: O Portal do Jubilamento - Diálogo")
    clock = pygame.time.Clock()
    
    caixa = CaixaDialogo(dialogo_data, screen, player_img_path, npc_img_path, bg_img_path)
    caixa.iniciar_dialogo()
    
    running = True
    completed = False
    
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if caixa.dialogo_ativo:
                        if caixa.avancar_fala():
                            completed = True
                            running = False
                elif evento.key == pygame.K_ESCAPE:
                    running = False
        
        caixa.atualizar()
        caixa.desenhar()
        pygame.display.flip()
        clock.tick(60)
    
    return completed


def _save_personagem_with_interactions(heroi):
    """Save personagem data including an `interactions` list (RU/Bowser events).

    Writes to `save_personagem.json` in the project base directory.
    """
    try:
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, 'save_personagem.json')
        # load existing if available to preserve other fields
        data = {}
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                data = {}

        # ensure basic personagem fields
        data.update({
            'nome': getattr(heroi, 'nome', ''),
            'vida': getattr(heroi, 'vida', 1),
            'defesa': getattr(heroi, 'defesa', 1),
            'ataque': getattr(heroi, 'ataque', 1),
            'iniciativa': getattr(heroi, 'iniciativa', 1),
            'dinheiro': getattr(heroi, 'dinheiro', 0),
            'estamina': getattr(heroi, 'estamina', 1),
            'encontrou_bowser': getattr(heroi, 'encontrou_bowser', 0)
        })

        # interactions
        interactions = getattr(heroi, 'interactions', []) or []
        data['interactions'] = interactions

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def dialogo_terreo():
    """Cena de diálogo no térreo com NPC."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
    npc_img = os.path.join(base, 'Imagens_dialogos', 'npc_sembg.png')
    bg_img = os.path.join(base, 'Imagens_dialogos', 'e378a975-e5d9-4162-98be-a6693a7d818a.jpg')
    return run_dialog_scene(DIALOGO_TERREO_INICIO, player_img, npc_img, bg_img)


def dialogo_intro_cleyton():
    """Cena de introdução com Mestre Cleyton."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
    bg_img = os.path.join(base, 'Imagens_dialogos', '854d6de6-6b65-4aca-9a57-65ebca4ceffa.jpg')
    return run_dialog_scene(DIALOGO_INTRO_MESTRE, player_img, None, bg_img)


def ru_choice_scene(heroi=None):
    """Mostra uma tela com opção de ir ao RU ou continuar para o próximo nível.

    Se o jogador escolher ir ao RU, existe chance de 3/10 de encontrar o Bowser.
    Em caso de encontro, apresenta diálogos e aplica consequências ao objeto `heroi`.
    """
    import random
    base = os.path.dirname(__file__)
    try:
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass
        screen = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
        pygame.display.set_caption('Decisão: RU ou Próximo Nível')
        clock = pygame.time.Clock()

        # tentar tocar a mesma música de fundo que o menu
        music_path = os.path.join(os.path.dirname(base), 'Sons', 'awesomeness.wav')
        if not os.path.exists(music_path):
            # procurar caminho relativo
            music_path = os.path.join(base, '..', 'Sons', 'awesomeness.wav')
        try:
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)
        except Exception:
            pass

        # simple UI
        font_large = pygame.font.SysFont(None, 36)
        font_small = pygame.font.SysFont(None, 24)

        btn_ru = pygame.Rect(220, 420, 260, 64)
        btn_next = pygame.Rect(540, 420, 260, 64)

        running = True
        result = {'choice': None, 'bowser': False, 'outcome': None}

        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if btn_ru.collidepoint(ev.pos):
                        result['choice'] = 'ru'
                        running = False
                    elif btn_next.collidepoint(ev.pos):
                        result['choice'] = 'next'
                        running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        running = False

            # draw
            screen.fill(AZUL_ESCURO)
            title_surf = pygame.font.SysFont(None, 36).render('Você encontrou Mestre Cleyton.', True, BRANCO)
            screen.blit(title_surf, (60, 80))
            sub_surf = pygame.font.SysFont(None, 26).render('Deseja ir ao Restaurante Universitário (RU) ou seguir para o próximo nível?', True, BRANCO)
            screen.blit(sub_surf, (60, 140))

            # buttons
            pygame.draw.rect(screen, (80, 160, 80), btn_ru, border_radius=8)
            pygame.draw.rect(screen, (80, 80, 200), btn_next, border_radius=8)
            ru_label = font_large.render('Ir para o RU', True, BRANCO)
            next_label = font_small.render('Continuar para o próximo nível', True, BRANCO)
            screen.blit(ru_label, (btn_ru.x + 40, btn_ru.y + 18))
            screen.blit(next_label, (btn_next.x + 10, btn_next.y + 18))

            pygame.display.flip()
            clock.tick(60)

        # se escolheu RU, rolar encontro com Bowser / ou seguir lógica do RU
        if result['choice'] == 'ru':
            # paths for images
            player_img = os.path.join(base, 'Imagens_dialogos', '14e0a435-3968-479c-be77-c7ff2173dd36.jpg')
            # preferir a imagem do Bowser que você colocou em `imagens_game`
            bowser_img = os.path.join(base, 'imagens_game', 'bowser_referencia.png')
            # fallback: se imagem específica do Bowser não existir, use outra imagem disponível
            if not os.path.exists(bowser_img):
                fallback1 = os.path.join(base, 'Imagens_dialogos', '80c5ae94-a3e5-4f61-8bce-44a89eefdbde.jpg')
                fallback2 = os.path.join(base, 'imagens_game', 'npc_sembg.png')
                if os.path.exists(fallback1):
                    bowser_img = fallback1
                elif os.path.exists(fallback2):
                    bowser_img = fallback2
                else:
                    bowser_img = None
            encontro_bg = os.path.join(base, 'Imagens_dialogos', 'encontro_bowser.jpg')
            ru_bg = os.path.join(base, 'imagens_game', 'RU.jpg')

            # integrate sistema_monetario pattern
            try:
                from personagem1 import preco_ru
            except Exception:
                preco_ru = 3.5

            # first: decide encounter probability
            encontro = random.randint(1, 10) <= 3  # 3/10 chance

            # if encounter happens immediately
            if encontro:
                result['bowser'] = True
                try:
                    from bowser import Bowser as BowserClass
                    texto = BowserClass.bowser_texto[0].get('aparição', '')
                except Exception:
                    texto = '...Um ser estranho aparece diante de você...'

                # parse bowser text into dialogue tuples to show Player and Bowser lines
                dialog_bowser = []
                for linha in texto.split('\n'):
                    linha = linha.strip()
                    if not linha:
                        continue
                    if linha.startswith('Você:'):
                        dialog_bowser.append(('Player', linha.partition(':')[2].strip()))
                    elif linha.startswith('Bowser:') or linha.startswith('???'):
                        # map Bowser/??? to Bowser
                        dialog_bowser.append(('Bowser', linha.partition(':')[2].strip()))
                    else:
                        # narration -> show as System (narrador), not Bowser
                        dialog_bowser.append(('System', linha))

                # show bowser scene with specific bg and images
                run_dialog_scene(dialog_bowser, player_img, bowser_img, encontro_bg)

                # call GUI roleta from bowser.py to apply effects
                try:
                    b = BowserClass(heroi)
                    res = b.rola_roleta_gui(texto)
                    escolha = res.get('escolha')
                    outcome_text = res.get('outcome_text', '')
                    texto_bowser = res.get('texto_bowser', '')
                except Exception:
                    escolha = None
                    outcome_text = ''
                    texto_bowser = ''

                # mark that bowser was encountered
                try:
                    setattr(heroi, 'encontrou_bowser', 1)
                except Exception:
                    pass

                # record interaction for Bowser
                try:
                    if not hasattr(heroi, 'interactions') or getattr(heroi, 'interactions') is None:
                        heroi.interactions = []
                    heroi.interactions.append({
                        'type': 'Bowser',
                        'when': datetime.now().isoformat(),
                        'context': 'aparição',
                        'texto_bowser': texto_bowser,
                        'escolha': escolha,
                        'outcome_text': outcome_text
                    })
                except Exception:
                    pass

                # persist hero changes
                try:
                    base_dir = os.path.dirname(__file__)
                    hero_data = {
                        'nome': getattr(heroi, 'nome', ''),
                        'vida': getattr(heroi, 'vida', 1),
                        'defesa': getattr(heroi, 'defesa', 1),
                        'ataque': getattr(heroi, 'ataque', 1),
                        'iniciativa': getattr(heroi, 'iniciativa', 1),
                        'estamina': getattr(heroi, 'estamina', 1),
                        'dinheiro': getattr(heroi, 'dinheiro', 0),
                        'nivel': getattr(heroi, 'nivel', 1),
                        'xp': getattr(heroi, 'xp', 0)
                    }
                    with open(os.path.join(base_dir, 'save_heroi.json'), 'w', encoding='utf-8') as f:
                        json.dump(hero_data, f, ensure_ascii=False, indent=2)

                    # save personagem including interactions
                    _save_personagem_with_interactions(heroi)
                except Exception:
                    pass

                # show result dialog
                resultado_dialog = [("Bowser", texto_bowser), ("System", escolha.get('nome') if escolha else ''), ("System", outcome_text)]
                run_dialog_scene(resultado_dialog, player_img, bowser_img, encontro_bg)

            else:
                # No immediate encounter: follow RU purchase flow (sistema_monetario)
                try:
                    from sistema_monetario import texto_ru, prato_aleatorio
                except Exception:
                    texto_ru = {'texto_chegando_ru': 'Você chega ao RU.' , 'texto_sem_evento': 'Nada de especial.'}
                    prato_aleatorio = 'Você comeu e se sentiu revigorado.'

                # show arrival on RU with RU background
                arrival_dialog = [("System", texto_ru.get('texto_chegando_ru', ''))]
                run_dialog_scene(arrival_dialog, player_img, None, ru_bg)

                # check money
                jogador_dinheiro = getattr(heroi, 'dinheiro', 0)
                if jogador_dinheiro < preco_ru:
                    # if hasn't met bowser before, trigger bowser encounter
                    if getattr(heroi, 'encontrou_bowser', 0) == 0:
                        try:
                            from bowser import Bowser as BowserClass
                            b = BowserClass(heroi)
                            # use re-aparição text
                            texto_re = BowserClass.bowser_texto[1].get('re-aparição', '')
                            # show bowser encounter
                            dialog_bowser = []
                            for linha in texto_re.split('\n'):
                                linha = linha.strip()
                                if not linha:
                                    continue
                                if linha.startswith('Você:'):
                                    dialog_bowser.append(('Player', linha.partition(':')[2].strip()))
                                elif linha.startswith('Bowser:') or linha.startswith('???'):
                                    dialog_bowser.append(('Bowser', linha.partition(':')[2].strip()))
                                else:
                                    # narration -> show as System (narrador), not Bowser
                                    dialog_bowser.append(('System', linha))
                            run_dialog_scene(dialog_bowser, player_img, bowser_img, encontro_bg)
                            res = b.rola_roleta_gui(texto_re)
                            # mark
                            try:
                                setattr(heroi, 'encontrou_bowser', 1)
                            except Exception:
                                pass
                            # record interaction
                            try:
                                if not hasattr(heroi, 'interactions') or getattr(heroi, 'interactions') is None:
                                    heroi.interactions = []
                                heroi.interactions.append({
                                    'type': 'Bowser',
                                    'when': datetime.now().isoformat(),
                                    'context': 're-aparição',
                                    'texto_bowser': res.get('texto_bowser', ''),
                                    'escolha': res.get('escolha'),
                                    'outcome_text': res.get('outcome_text', '')
                                })
                            except Exception:
                                pass
                            # save hero and personagem with interactions
                            try:
                                base_dir = os.path.dirname(__file__)
                                with open(os.path.join(base_dir, 'save_heroi.json'), 'w', encoding='utf-8') as f:
                                    json.dump({'nome': heroi.nome, 'vida': heroi.vida, 'defesa': heroi.defesa, 'ataque': heroi.ataque, 'iniciativa': heroi.iniciativa, 'estamina': heroi.estamina, 'dinheiro': heroi.dinheiro}, f, ensure_ascii=False, indent=2)
                            except Exception:
                                pass
                            _save_personagem_with_interactions(heroi)
                            # show result
                            resultado_dialog = [("Bowser", res.get('texto_bowser', '')), ("System", res.get('escolha', {}).get('nome', '')), ("System", res.get('outcome_text', ''))]
                            run_dialog_scene(resultado_dialog, player_img, bowser_img, encontro_bg)
                        except Exception:
                            # fallback: show no event and record RU interaction (no money, no Bowser)
                            try:
                                if not hasattr(heroi, 'interactions') or getattr(heroi, 'interactions') is None:
                                    heroi.interactions = []
                                heroi.interactions.append({
                                    'type': 'RU',
                                    'when': datetime.now().isoformat(),
                                    'action': 'no_money',
                                    'preco': preco_ru,
                                    'encontrou_bowser': getattr(heroi, 'encontrou_bowser', 0)
                                })
                                _save_personagem_with_interactions(heroi)
                            except Exception:
                                pass
                            run_dialog_scene([("System", texto_ru.get('texto_sem_evento', ''))], player_img, None, ru_bg)
                    else:
                        # record RU no-money but already met Bowser (no new event)
                        try:
                            if not hasattr(heroi, 'interactions') or getattr(heroi, 'interactions') is None:
                                heroi.interactions = []
                            heroi.interactions.append({
                                'type': 'RU',
                                'when': datetime.now().isoformat(),
                                'action': 'no_money_already_met_bowser',
                                'preco': preco_ru,
                                'encontrou_bowser': getattr(heroi, 'encontrou_bowser', 0)
                            })
                            _save_personagem_with_interactions(heroi)
                        except Exception:
                            pass
                        run_dialog_scene([("System", texto_ru.get('texto_sem_evento', ''))], player_img, None, ru_bg)
                else:
                    # player has money: ask to buy (simple GUI yes/no)
                    buying = True
                    buy_choice = None
                    # create simple buttons
                    btn_yes = pygame.Rect(300, 480, 160, 56)
                    btn_no = pygame.Rect(560, 480, 160, 56)
                    while buying:
                        for ev in pygame.event.get():
                            if ev.type == pygame.QUIT:
                                buying = False
                            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                                if btn_yes.collidepoint(ev.pos):
                                    buy_choice = True
                                    buying = False
                                elif btn_no.collidepoint(ev.pos):
                                    buy_choice = False
                                    buying = False
                        screen.fill(AZUL_ESCURO)
                        prompt = pygame.font.SysFont(None, 28).render(f'Comprar ticket para comer por R$ {preco_ru:.2f}?', True, BRANCO)
                        screen.blit(prompt, (220, 360))
                        pygame.draw.rect(screen, (80,200,80), btn_yes, border_radius=8)
                        pygame.draw.rect(screen, (200,80,80), btn_no, border_radius=8)
                        screen.blit(pygame.font.SysFont(None, 26).render('Sim', True, BRANCO), (btn_yes.x+50, btn_yes.y+16))
                        screen.blit(pygame.font.SysFont(None, 26).render('Não', True, BRANCO), (btn_no.x+60, btn_no.y+16))
                        pygame.display.flip()
                        clock.tick(30)

                    if buy_choice:
                        # pay and restore
                        try:
                            dinheiro_before = getattr(heroi, 'dinheiro', 0)
                            heroi.pagar_ru()
                        except Exception:
                            dinheiro_before = getattr(heroi, 'dinheiro', 0)
                            heroi.dinheiro = dinheiro_before - preco_ru
                        dinheiro_after = getattr(heroi, 'dinheiro', 0)
                        heroi.vida = getattr(heroi, 'vidabase', getattr(heroi, 'vida', 1))
                        heroi.estamina = getattr(heroi, 'estaminabase', getattr(heroi, 'estamina', 1))
                        # show plate dialog
                        run_dialog_scene([("Player", prato_aleatorio)], player_img, None, ru_bg)
                        # record RU purchase interaction
                        try:
                            if not hasattr(heroi, 'interactions') or getattr(heroi, 'interactions') is None:
                                heroi.interactions = []
                            heroi.interactions.append({
                                'type': 'RU',
                                'when': datetime.now().isoformat(),
                                'action': 'buy',
                                'preco': preco_ru,
                                'dinheiro_before': dinheiro_before,
                                'dinheiro_after': dinheiro_after,
                                'prato': prato_aleatorio
                            })
                        except Exception:
                            pass
                        # save personagem with interactions
                        _save_personagem_with_interactions(heroi)
                        # if previously met Bowser, he can reappear
                        if getattr(heroi, 'encontrou_bowser', 0) == 1:
                            try:
                                from bowser import Bowser as BowserClass
                                b = BowserClass(heroi)
                                texto_re = BowserClass.bowser_texto[1].get('re-aparição', '')
                                dialog_bowser = []
                                for linha in texto_re.split('\n'):
                                    linha = linha.strip()
                                    if not linha:
                                        continue
                                    if linha.startswith('Você:'):
                                        dialog_bowser.append(('Player', linha.partition(':')[2].strip()))
                                    elif linha.startswith('Bowser:') or linha.startswith('???'):
                                        dialog_bowser.append(('Bowser', linha.partition(':')[2].strip()))
                                    else:
                                        # narration -> show as System (narrador), not Bowser
                                        dialog_bowser.append(('System', linha))
                                run_dialog_scene(dialog_bowser, player_img, bowser_img, encontro_bg)
                                res = b.rola_roleta_gui(texto_re)
                                # record interaction + save
                                try:
                                    if not hasattr(heroi, 'interactions') or getattr(heroi, 'interactions') is None:
                                        heroi.interactions = []
                                    heroi.interactions.append({
                                        'type': 'Bowser',
                                        'when': datetime.now().isoformat(),
                                        'context': 're-aparição_after_ru',
                                        'texto_bowser': res.get('texto_bowser', ''),
                                        'escolha': res.get('escolha'),
                                        'outcome_text': res.get('outcome_text', '')
                                    })
                                except Exception:
                                    pass
                                _save_personagem_with_interactions(heroi)
                                resultado_dialog = [("Bowser", res.get('texto_bowser', '')), ("System", res.get('escolha', {}).get('nome', '')), ("System", res.get('outcome_text', ''))]
                                run_dialog_scene(resultado_dialog, player_img, bowser_img, encontro_bg)
                            except Exception:
                                pass

        # parar música e sair (não quit para não finalizar subsistema de vídeo do jogo)
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        return result

        return result
    except Exception:
        return {'choice': None}


def dialogo_nivel_1():
    """Cena de diálogo: Nível 1 - Goblin da Administração."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
    npc_img = os.path.join(base, 'imagens_sem_bg', 'goblin_adm.png')
    return run_dialog_scene(DIALOGO_NIVEL_1_CHEFE, player_img, npc_img)


def dialogo_pos_nivel_1():
    """Cena pós-batalha: Nível 1 com Mestre Cleyton."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
    bg_img = os.path.join(base, 'Imagens_dialogos', '854d6de6-6b65-4aca-9a57-65ebca4ceffa.jpg')
    return run_dialog_scene(DIALOGO_POS_NIVEL_1, player_img, None, bg_img)


def dialogo_nivel_2():
    """Cena de diálogo: Nível 2 - Robô Natureza."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
    npc_img = os.path.join(base, 'imagens_sem_bg', 'robo_sustentavel.png')
    return run_dialog_scene(DIALOGO_NIVEL_2_CHEFE, player_img, npc_img)


def dialogo_pos_nivel_2():
    """Cena pós-batalha: Nível 2 com Mestre Cleyton."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
    bg_img = os.path.join(base, 'Imagens_dialogos', '854d6de6-6b65-4aca-9a57-65ebca4ceffa.jpg')
    return run_dialog_scene(DIALOGO_POS_NIVEL_2, player_img, None, bg_img)


def dialogo_nivel_3():
    """Cena de diálogo: Nível 3 - Mago Místico."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
    npc_img = os.path.join(base, 'imagens_sem_bg', 'mago_matematica.png')
    return run_dialog_scene(DIALOGO_NIVEL_3_CHEFE, player_img, npc_img)


def dialogo_pos_nivel_3():
    """Cena pós-batalha: Nível 3 com Mestre Cleyton."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
    bg_img = os.path.join(base, 'Imagens_dialogos', '854d6de6-6b65-4aca-9a57-65ebca4ceffa.jpg')
    return run_dialog_scene(DIALOGO_POS_NIVEL_3, player_img, None, bg_img)


def dialogo_nivel_4():
    """Cena de diálogo: Nível 4 - Robô Python."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'imagens_game', 'miguel_sembg.png')
    npc_img = os.path.join(base, 'imagens_sem_bg', 'robo_python.png')
    return run_dialog_scene(DIALOGO_NIVEL_4_CHEFE, player_img, npc_img)


def dialogo_conclusao():
    """Cena final: Conclusão com Mestre Cleyton."""
    base = os.path.dirname(__file__)
    player_img = os.path.join(base, 'Imagens_dialogos', '14e0a435-3968-479c-be77-c7ff2173dd36.jpg')
    bg_img = os.path.join(base, 'Imagens_dialogos', '854d6de6-6b65-4aca-9a57-65ebca4ceffa.jpg')
    return run_dialog_scene(DIALOGO_CONCLUSAO, player_img, None, bg_img)


if __name__ == '__main__':
    # Test: run terreo dialog
    dialogo_terreo()
