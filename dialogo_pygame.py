import pygame
import sys
import time

# --- Configurações Básicas do Pygame ---
pygame.init()
TELA_LARGURA = 800
TELA_ALTURA = 600
TELA = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption("CEAGRI: O Portal do Jubilamento")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL_ESCURO = (15, 32, 60) # Cor de fundo principal
AZUL_CLARO = (80, 150, 220) # Cor para a borda
CINZA_TRANSPARENTE = (0, 0, 0, 220) # Fundo da caixa de diálogo
VERDE_TEXTO = (150, 255, 150) # Texto de "código"
LARANJA_TEXTO = (255, 170, 0) # Nome do personagem

# Fonte
pygame.font.init()
# Tenta usar uma fonte que pareça mais "jogo" se disponível, senão usa a padrão.
try:
    FONTE_FALA = pygame.font.Font(pygame.font.get_default_font(), 24)
    FONTE_NOME = pygame.font.Font(pygame.font.get_default_font(), 20)
except:
    FONTE_FALA = pygame.font.SysFont('Arial', 24)
    FONTE_NOME = pygame.font.SysFont('Arial', 20)
    print("Usando fonte padrão do sistema.")


# --- Dados do Diálogo (Seu Roteiro Completo) ---
DIALOGUE_SCRIPT = [
    # Térreo - Início
    {"personagem": "Player", "fala": "Mais um dia de aula. Estou quase terminando o último período, finalmente!!"},
    {"personagem": "Player", "fala": "Falta apenas eu terminar meu TCC."},
    {"personagem": "Player", "fala": "Oxente, cadê todo mundo?"},
    {"personagem": "NPC", "fala": "Você não ficou sabendo?"},
    {"personagem": "Player", "fala": "Sabendo de que? Não tem aula hoje?"},
    {"personagem": "NPC", "fala": "Não vai ter aula durante um bom tempo, os professores entraram em greve."},
    {"personagem": "Player", "fala": "GREVE!? MAS PORQUE?!"},
    {"personagem": "NPC", "fala": "Calma, vou explicar, mas não fica com raiva."},
    {"personagem": "Player", "fala": "*suspira...* Tá. Explica o motivo dessa greve."},
    {"personagem": "NPC", "fala": "Aparentemente, um aluno... estava cansado de repetir de cadeira. Ele repetiu a mesma umas 3 vezes, e outras duas, ele repetiu 2 vezes."},
    {"personagem": "NPC", "fala": "Ele surtou, ficou cansado dessa situação e decidiu que ia mudar isso de uma vez por todas."},
    {"personagem": "Player", "fala": "E o que ele fez? Porque eu nessa situação trancaria e faria ENEM de novo. Tá maluco, repetir tantas vezes assim."},
    {"personagem": "NPC", "fala": "Ele procurou na *dark web*, rituais de estudantes universitários que mexem com magia negra. Procurou um ritual que o faria se formar rapidamente."},
    {"personagem": "Player", "fala": "Que? Isso existe mesmo?"},
    {"personagem": "NPC", "fala": "Aparentemente sim. Porém, o ritual provavelmente deu errado, ou ele fez outro ritual."},
    {"personagem": "Player", "fala": "Como assim?"},
    {"personagem": "NPC", "fala": "Ele recitou palavras estranhas, usou algumas oferendas para seres de outro mundo. E... e...."},
    {"personagem": "Player", "fala": "E O QUE?!!!!"},
    {"personagem": "NPC", "fala": "E abriu um portal interdimensional, que mudou o espaço tempo, as cadeiras se materializaram como monstros."},
    {"personagem": "Player", "fala": "QUE? E COMO QUE TU SABE DE TUDO ISSO? ESPAÇO TEMPO? EU NÃO ENTENDI NADA!"},
    {"personagem": "NPC", "fala": "Eu assisti muito filme de ficção científica, eu sei o que eu tô falando!"},
    {"personagem": "Player", "fala": "Tá, mas e aí? O que aconteceu depois?"},
    {"personagem": "NPC", "fala": "Os monstros estão oferecendo perigo para o nosso prédio, o governo ainda não veio ver."},
    {"personagem": "Player", "fala": "E porque não?"},
    {"personagem": "NPC", "fala": "A greve dos professores começou a pouco tempo, eles estavam assustados com essa situação. Então o governo ainda não sabe bem o motivo da greve."},
    {"personagem": "Player", "fala": "Entendi! A gente tem que fazer algo a respeito."},
    {"personagem": "NPC", "fala": "Oxe? Como assim? Você vai conseguir derrotar esses monstros?"},
    {"personagem": "Player", "fala": "Tenho que tentar! Eu não posso demorar, eu tô fazendo estágio em uma empresa renomada e falei pra eles que faltava pouco pra me formar."},
    {"personagem": "Player", "fala": "Tenho que me formar logo pra ser efetivado(a)!!"},
    {"personagem": "NPC", "fala": "Rapaz, boa sorte, pois eu não faço ideia de como fazer isso!"},
    {"personagem": "Player", "fala": "Bem, como um(a) jogador(a) de RPG, eu diria que o prédio virou uma espécie de masmorra, conhecida como 'dungeon'. Se eu derrotar os monstros e fechar o portal. Provavelmente vai tudo voltar ao normal!"},

    # --- Transição / Cleyton ---
    {"personagem": "Mestre Cleyton", "fala": "Jovem herói/heroína, finalmente nos encontramos. Eu sou Cleyton. Eu sou um Guia Dimensional. O que você viu é a materialização do Cáos Curricular."},
    {"personagem": "Mestre Cleyton", "fala": "O CEAGRI, seu templo de conhecimento, agora é uma Masmorra Acadêmica. Sua missão é simples: Você deve derrotar as quatro Entidades e, com a essência de cada uma, fechar o Portal do Jubilamento, antes que o Cáos se espalhe para o mundo exterior."},
    {"personagem": "Mestre Cleyton", "fala": "Para chegar ao Portal, você deve provar seu valor: Nível 1: Derrote o Goblin da Administração para recuperar a Ordem Burocrática."},
    {"personagem": "Mestre Cleyton", "fala": "Nível 2: Derrote o Robô Natureza da Sustentabilidade para reestabelecer o Equilíbrio dos Recursos."},
    {"personagem": "Mestre Cleyton", "fala": "Nível 3: Derrote o Mago Místico da Matemática Discreta para restaurar a Lógica da Estrutura."},
    {"personagem": "Mestre Cleyton", "fala": "Seu primeiro passo está no primeiro andar. Que a sabedoria o guie!"},

    # --- Nível 1: Diálogo com o Chefe ---
    {"personagem": "Goblin da Adm.", "fala": "HAH! Mais um calouro perdido na burocracia eterna! Você será um escravo da papelada, como todos nós!"},
    {"personagem": "Player", "fala": "Calouro é a sua avó, seu duende da papelada! Eu vim aqui para desburocratizar essa bagunça! Eu só quero meu diploma!"},
    {"personagem": "Goblin da Adm.", "fala": "Acha que é fácil? Já preencheu o formulário 38-B para solicitação de diploma? Você nunca passará por mim sem uma assinatura e três cópias autenticadas! Muahahah!"},
    {"personagem": "Player", "fala": "Não mesmo! Prepare-se para ser arquivado no lixo da história, seu mestre da papelada!"},

    # --- Pós-Batalha Nível 1 ---
    {"personagem": "Mestre Cleyton", "fala": "Parabéns! Você arquivou com sucesso o primeiro desafio. A essência da Administração está agora em suas mãos. Batalhas consomem energia. Se precisar reabastecer seus recursos, pressione [ESPAÇO] e reinicie o diálogo."},
    {"personagem": "Mestre Cleyton", "fala": "Sua próxima prova é o dilema do mundo moderno: Sustentabilidade."},

    # --- Nível 2: Diálogo com o Chefe ---
    {"personagem": "Robô Natureza", "fala": "Invasor. Seu carbono footprint está muito alto. Humanidade é um vírus. Este andar será o primeiro estágio."},
    {"personagem": "Player", "fala": "Olha, eu apoio a sustentabilidade, juro! Eu separo meu lixo e uso ecobag! Mas transformar o prédio em uma selva não vai me impedir de terminar o TCC!"},
    {"personagem": "Robô Natureza", "fala": "Insuficiente. Seu 'TCC' é uma manifestação da exploração dos recursos. Mais papel. Você será compostado, elemento disruptivo!"},
    {"personagem": "Player", "fala": "Reciclado é o seu conceito de justiça ambiental! Eu vou mostrar a você o verdadeiro poder de um humano que quer se formar!"},

    # --- Pós-Batalha Nível 2 ---
    {"personagem": "Mestre Cleyton", "fala": "Excelente! Você reciclou seu caminho para a vitória! O Equilíbrio dos Recursos foi restaurado. A pressão acadêmica é forte. É sábio fazer uma pausa. Pressione [ESPAÇO] para simular a subida ou volta."},
    {"personagem": "Mestre Cleyton", "fala": "Agora, você enfrenta a essência da Lógica e da Estrutura. O terceiro andar é o domínio da Matemática Discreta. Lembre-se: Seu ponto fraco é a falha na lógica."},

    # --- Nível 3: Diálogo com o Chefe ---
    {"personagem": "Mago Místico", "fala": "Mais um que ousa desafia a Lógica Inerente. Você busca o caos na Ordem Perfeita dos Grafos?"},
    {"personagem": "Player", "fala": "A única coisa que eu quero é entender como fechar esse portal e me livrar de você, seu feiticeiro dos números!"},
    {"personagem": "Mago Místico", "fala": "Eu sou a manifestação da Pura Dedução. Sua busca por um 'diploma' é um algoritmo com variáveis não definidas. Você será apenas mais uma variável em minha equação da eternidade!"},
    {"personagem": "Player", "fala": "Ah é? Então prepare-se para ser a variável 'x' que eu vou isolar e eliminar!"},

    # --- Pós-Batalha Nível 3 ---
    {"personagem": "Mestre Cleyton", "fala": "Você superou a Complexidade! Sua mente é tão afiada quanto uma demonstração por indução! A Lógica da Estrutura está agora com você. Este é o ponto sem volta."},
    {"personagem": "Mestre Cleyton", "fala": "O Robô Robust Python espera. Ele é a manifestação da linguagem que deu origem a todo o programa. Seu único caminho é encontrar o Bug."},

    # --- Nível 4: Diálogo com o Boss Final ---
    {"personagem": "Robô Python", "fala": "print(\"Intruso detectado. Inicializando protocolo de eliminação.\")"},
    {"personagem": "Player", "fala": "Então você é o chefão, hein? O Guardião do Código que está por trás de toda essa bagunça!"},
    {"personagem": "Robô Python", "fala": "Error: Argumento inválido. Não sou \"chefão\". Sou a Arquitetura Principal. Sua presença causa conflito de recursos."},
    {"personagem": "Player", "fala": "Um script com erros? Eu sou o aluno que vai te desinstalar! Você não possui as bibliotecas necessárias para me derrotar!"},
    {"personagem": "Robô Python", "fala": "Minha lógica é impecável. Você não possui as bibliotecas necessárias para me derrotar. Import 'derrota' as 'sua_derrota'."},
    {"personagem": "Player", "fala": "Pode ser que eu não tenha todas as bibliotecas, mas eu tenho a determinação de um estudante que não quer ser jubilado! Prepare-se para um *traceback* que você nunca vai esquecer!"},

    # --- Conclusão ---
    {"personagem": "Mestre Cleyton", "fala": "Você conseguiu! Você superou o Cáos Curricular!"},
    {"personagem": "Player", "fala": "Eu... eu achei o Bug dele. Uma falha de lógica na... na declaração de variáveis! Agora, como eu fecho essa aberração?"},
    {"personagem": "Mestre Cleyton", "fala": "As quatro essências — Ordem, Equilíbrio, Lógica e Código — são as chaves. Use-as para reescrever o código de existência do portal."},
    {"personagem": "Player", "fala": "Vai! portal.close()!"},
    {"personagem": "Mestre Cleyton", "fala": "É isso! O tempo e o espaço foram restaurados. Os professores voltarão amanhã, e a greve será esquecida como um erro de digitação."},
    {"personagem": "Player", "fala": "Eu consegui! Estou formado(a)! Efetivação, lá vou eu!"},
    {"personagem": "Mestre Cleyton", "fala": "Lembre-se, jovem herói/heroína, o verdadeiro poder está em não desistir da sua formação. Agora vá. Sua jornada acadêmica terminou."},
    
    # Fim do Diálogo
    {"personagem": "FIM", "fala": "Diálogo concluído. Pressione [ESPAÇO] para reiniciar ou [ESC] para sair."},
]


class CaixaDialogo:
    """Gerencia e desenha a caixa de diálogo com efeito typewriter."""
    def __init__(self, dialogo_data, tela):
        self.dialogo_data = dialogo_data
        self.tela = tela
        
        # Estado do Diálogo
        self.dialogo_ativo = False
        self.indice_fala = 0 # Índice da fala atual
        
        # Configurações da Caixa de Diálogo
        self.altura_caixa = 150
        self.margem_x = 50
        self.caixa_rect = pygame.Rect(self.margem_x, TELA_ALTURA - self.altura_caixa, 
                                      TELA_LARGURA - 2 * self.margem_x, self.altura_caixa - 20)
        
        # Configurações do Typewriter (Digitação Lenta)
        self.texto_exibido = ""
        self.indice_letra = 0
        self.velocidade_digitacao = 0.02 # Tempo em segundos entre cada letra
        self.ultima_atualizacao = time.time()
        self.animacao_completa = False # Se toda a fala já foi exibida

    def iniciar_dialogo(self):
        """Inicia o diálogo na primeira fala."""
        if not self.dialogo_ativo:
            self.dialogo_ativo = True
            self.indice_fala = 0
            self._resetar_fala()

    def _resetar_fala(self):
        """Prepara o estado para a nova fala."""
        if self.indice_fala < len(self.dialogo_data):
            self.texto_exibido = ""
            self.indice_letra = 0
            self.animacao_completa = False

    def avancar_fala(self):
        """Avança para a próxima fala ou encerra o diálogo."""
        if not self.dialogo_ativo:
            return

        if self.animacao_completa:
            # 1. Se a animação estiver completa, avança para o próximo diálogo
            self.indice_fala += 1
            if self.indice_fala >= len(self.dialogo_data):
                # Opcional: manter a última fala em tela
                self.dialogo_ativo = True 
                self.indice_fala = len(self.dialogo_data) - 1
            else:
                self._resetar_fala()
        else:
            # 2. Se a animação NÃO estiver completa, pula para o texto final
            if self.indice_fala < len(self.dialogo_data):
                self.texto_exibido = self.dialogo_data[self.indice_fala]['fala']
                self.animacao_completa = True
                self.indice_letra = len(self.texto_exibido)


    def atualizar(self):
        """Atualiza a animação de digitação (Typewriter)."""
        if not self.dialogo_ativo or self.animacao_completa:
            return

        # Garante que o índice está dentro dos limites
        if self.indice_fala >= len(self.dialogo_data):
             return 

        fala_atual = self.dialogo_data[self.indice_fala]['fala']
        
        if time.time() - self.ultima_atualizacao > self.velocidade_digitacao:
            if self.indice_letra < len(fala_atual):
                # Adiciona a próxima letra
                self.texto_exibido += fala_atual[self.indice_letra]
                self.indice_letra += 1
            else:
                # A fala terminou de ser digitada
                self.animacao_completa = True
            
            self.ultima_atualizacao = time.time()


    def desenhar(self):
        """Desenha a caixa, o nome do personagem e o texto atual."""
        if not self.dialogo_ativo:
            return

        # Garante que o índice está dentro dos limites (em caso de reinício)
        if self.indice_fala >= len(self.dialogo_data):
             self.indice_fala = len(self.dialogo_data) - 1

        fala_atual = self.dialogo_data[self.indice_fala]
        
        # --- 1. Desenhar a Caixa de Fundo Semi-Transparente ---
        # Cria uma superfície com canal Alpha (transparência)
        superficie_fundo = pygame.Surface((self.caixa_rect.width, self.caixa_rect.height), pygame.SRCALPHA)
        superficie_fundo.fill(CINZA_TRANSPARENTE)
        
        # Desenha a borda da caixa
        pygame.draw.rect(superficie_fundo, AZUL_CLARO, (0, 0, self.caixa_rect.width, self.caixa_rect.height), 3, border_radius=10)
        
        self.tela.blit(superficie_fundo, (self.caixa_rect.x, self.caixa_rect.y))

        # --- 2. Desenhar o Nome do Personagem (Balão) ---
        nome_renderizado = FONTE_NOME.render(fala_atual['personagem'], True, BRANCO)
        
        # Posição do nome acima e à esquerda da caixa
        pos_nome_x = self.caixa_rect.x + 10
        pos_nome_y = self.caixa_rect.y - 30
        
        # Desenha um pequeno "balão" para o nome
        balao_nome_rect = nome_renderizado.get_rect(topleft=(pos_nome_x, pos_nome_y))
        balao_nome_rect.inflate_ip(10, 5) # Aumenta um pouco o balão
        pygame.draw.rect(TELA, LARANJA_TEXTO, balao_nome_rect, border_radius=5)
        TELA.blit(nome_renderizado, (pos_nome_x + 5, pos_nome_y + 2)) # Desenha o texto do nome

        # --- 3. Desenhar o Texto da Fala (Multilinha se necessário) ---
        self._desenhar_texto_multilinha(self.texto_exibido, 
                                        self.caixa_rect.x + 15, 
                                        self.caixa_rect.y + 15, 
                                        self.caixa_rect.width - 30)
        
        # --- 4. Desenhar Indicador de Próxima Fala (se a animação estiver completa) ---
        if self.animacao_completa:
            # Indicador "Pressione ENTER"
            indicador_texto = FONTE_NOME.render("[ENTER] para Continuar", True, AZUL_CLARO)
            # Triângulo indicador (visual)
            indicador_triangulo = FONTE_NOME.render("▼", True, BRANCO) 
            
            # Posição para o triângulo
            pos_triangulo = (self.caixa_rect.right - 25, self.caixa_rect.bottom - 25)
            TELA.blit(indicador_triangulo, pos_triangulo)
            
            # Posição para o texto
            pos_texto = (self.caixa_rect.right - indicador_texto.get_width() - 5, self.caixa_rect.bottom + 5)
            #TELA.blit(indicador_texto, pos_texto)
    

    def _desenhar_texto_multilinha(self, texto, x, y, max_largura):
        """Função utilitária para quebrar e desenhar texto longo."""
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ''
        
        # Cor de texto padrão
        cor_fala = BRANCO
        if "Robô Python" in self.dialogo_data[self.indice_fala]['personagem']:
             cor_fala = VERDE_TEXTO # Cor diferente para o código
        
        for palavra in palavras:
            temp_linha = linha_atual + palavra + ' '
            # Verifica se a nova linha (incluindo a palavra) excede a largura máxima
            if FONTE_FALA.size(temp_linha)[0] < max_largura:
                linha_atual = temp_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + ' '
        linhas.append(linha_atual) # Adiciona a última linha
        
        # Desenha as linhas
        for i, linha in enumerate(linhas):
            texto_renderizado = FONTE_FALA.render(linha.strip(), True, cor_fala)
            self.tela.blit(texto_renderizado, (x, y + i * 30))


# --- Loop Principal do Jogo ---

caixa_dialogo = CaixaDialogo(DIALOGUE_SCRIPT, TELA)
# Inicia o diálogo imediatamente para mostrar a história
caixa_dialogo.iniciar_dialogo() 

clock = pygame.time.Clock()
running = True

while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        
        # Manipulação de eventos para o diálogo
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                # ENTER: Avança a fala (ou pula a animação)
                if caixa_dialogo.dialogo_ativo:
                    caixa_dialogo.avancar_fala()
            
            if evento.key == pygame.K_SPACE:
                # ESPAÇO: Reinicia o diálogo (simula voltar ao Térreo)
                caixa_dialogo.iniciar_dialogo()

            if evento.key == pygame.K_ESCAPE:
                running = False


    # --- Lógica de Atualização ---
    caixa_dialogo.atualizar() # Atualiza o efeito de digitação

    # --- Renderização ---
    # Fundo do CEAGRI (um fundo temático)
    TELA.fill(AZUL_ESCURO) 
    
    # Adiciona uma mensagem de instrução
    instrucao_texto = "Pressione [ENTER] para avançar. [ESPAÇO] para reiniciar a aventura."
    instrucao_render = FONTE_NOME.render(instrucao_texto, True, BRANCO)
    TELA.blit(instrucao_render, (TELA_LARGURA // 2 - instrucao_render.get_width() // 2, 20))


    # Desenha a caixa de diálogo por cima de tudo
    caixa_dialogo.desenhar() 

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60) # Limita o FPS a 60

pygame.quit()
sys.exit()