# game_assets.py

# ==========================================================
# Placeholder para Personagem. Eu vou assumir que você tem 
# as classes Heroi e Personagem importáveis.
# Se precisar, descomente e use esta classe mock:
# class MockPersonagem:
#     def __init__(self, nome, vida, ataque, defesa, estamina, carga):
#         self.nome = nome
#         self.vida = vida
#         self.vidabase = vida
#         self.ataque = ataque
#         self.defesa = defesa
#         self.estamina = estamina
#         self.estaminabase = estamina
#         self.carga_especial = carga
#         self.carga_max_especial = 100
#         self.trufa = [] # Simplificado para o mock
# ==========================================================


# Diálogos e Dados dos Chefes
BOSSES_DATA = {
    "Administracao": {
        "nome": "Goblin da Administração",
        "bg_image": "imagens_game/corredor_administracao.png", # PLACEHOLDER
        "sprite_enemy": "imagens_boss/goblin_admin.png",       # PLACEHOLDER
        "sprite_hero": "imagens_heroi/hero_parado.png",        # PLACEHOLDER
        "stats": (150, 20, 10, 5, 0), # Vida, Ataque, Defesa, Estamina, Carga
        "dialogue": [
            {"speaker": "Goblin da Administração", "text": "HAH! Mais um calouro perdido na burocracia eterna! Ou seria um quase-formando? Não importa! Todos se submeterão à Ordem dos Formulários Indefinidos!"},
            {"speaker": "Player", "text": "Calouro é a sua avó, seu duende da papelada! E eu não vou me submeter a nada, muito menos a você e suas pilhas de documentos sem fim! Eu só quero meu diploma!"},
            {"speaker": "Goblin da Administração", "text": "Diploma? HA! Acha que é fácil assim? Já preencheu o formulário 38-B para solicitação de diploma? E a taxa de homologação? Está atualizada? E a cópia autenticada do histórico escolar?!"},
            {"speaker": "Player", "text": "Que formulário o quê! Eu já preenchi tudo isso! Minha documentação está perfeita! E a minha vida não vai virar uma pilha de papéis por sua causa!"},
            {"speaker": "Goblin da Administração", "text": "Ah, mas vai! Cada papel que você arquivar, cada xerox que você fizer, cada carimbo que você pedir… é um pequeno pedaço da sua alma que me pertence! Você será um escravo da papelada, como todos nós!"},
            {"speaker": "Player", "text": "Não mesmo! Eu vim aqui para **desburocratizar** essa bagunça! Prepare-se para ser arquivado no lixo da história, seu mestre da papelada!"},
            {"speaker": "Goblin da Administração", "text": "Tente, se puder! Minha força vem da sua procrastinação e do seu ódio por filas e documentos! Você nunca passará por mim sem uma assinatura e três cópias autenticadas! Muahahah!"},
            {"speaker": "SYSTEM", "text": "Início da batalha contra o Chefe da Administração!"}
        ],
    },
    "Sustentabilidade": {
        "nome": "Robô Natureza",
        "bg_image": "imagens_game/corredor_sustentabilidade.png", # PLACEHOLDER
        "sprite_enemy": "imagens_boss/robo_natureza.png",        # PLACEHOLDER
        "sprite_hero": "imagens_heroi/hero_parado.png",         # PLACEHOLDER
        "stats": (200, 25, 15, 4, 0),
        "dialogue": [
            {"speaker": "Robô Natureza", "text": "Invasor. Seu carbono footprint está muito alto. Você é uma ameaça ao equilíbrio do ecossistema. Consumir. Produzir. Descartar. O ciclo deve ser quebrado."},
            {"speaker": "Player", "text": "Caramba, que papo é esse? Olha, eu apoio a sustentabilidade, juro! Eu separo meu lixo, uso ecobag e até desligo a luz quando saio!"},
            {"speaker": "Robô Natureza", "text": "Insuficiente. Seus sistemas são falhos. Humanidade é um vírus. Consome recursos sem regeneração. Este andar será o primeiro estágio. Toda a faculdade será reabsorvida pela natureza. A tecnologia corrompida será purificada."},
            {"speaker": "Player", "text": "Purificada? Você está transformando o prédio em uma selva e empilhando lixo eletrônico como se fosse arte! Isso não é sustentabilidade, é uma bagunça que vai me impedir de terminar o TCC!"},
            {"speaker": "Robô Natureza", "text": "Seu 'TCC' é uma manifestação da exploração dos recursos. Mais papel. Mais energia. Mais dados. Tudo para a sua 'formação'. A formação verdadeira é retornar ao pó."},
            {"speaker": "Player", "text": "Ei, calma lá! Minha formação é importante pra eu ter uma vida decente e, quem sabe, até desenvolver soluções mais sustentáveis no futuro! Você está deturpando tudo!"},
            {"speaker": "Robô Natureza", "text": "Deturpando? Eu sou a verdade bruta. A regeneração através da destruição do ciclo vicioso. Prepare-se para ser compostado, elemento disruptivo! Sua energia será reciclada."},
            {"speaker": "Player", "text": "Reciclado é o seu conceito de justiça ambiental! Eu vou mostrar a você o verdadeiro poder de um humano que quer se formar e ainda se importa com o planeta! Vamos lá, ô 'Mestre Verde'!"},
            {"speaker": "SYSTEM", "text": "Início da batalha contra o Chefe da Sustentabilidade!"}
        ],
    },
    # ... (Os outros chefes seguem o mesmo padrão)
    "Matematica": {
        "nome": "Mago Místico",
        "bg_image": "imagens_game/corredor_matematica.png",
        "sprite_enemy": "imagens_boss/mago_mistico.png",
        "sprite_hero": "imagens_heroi/hero_parado.png",
        "stats": (250, 30, 20, 6, 0),
        "dialogue": [
            {"speaker": "Mago Místico", "text": "Mais um que ousa desafiar a Lógica Inerente. Você busca o caos na Ordem Perfeita dos Grafos? Ignora as Conexões e Provações?"},
            {"speaker": "Player", "text": "Lógica? Ordem? A única coisa que eu quero é entender como fechar esse portal e me livrar de você, seu feiticeiro dos números!"},
            {"speaker": "Mago Místico", "text": "Feiticeiro? Eu sou a manifestação da Pura Dedução. Cada vértice, cada aresta, cada equação diferencial... são fios que tecem a realidade. Você está preso em uma teia de axiomas insolúveis."},
            {"speaker": "Player", "text": "Axiomas insolúveis sou eu tentando entender a sua disciplina quando o professor só fala com as costas para o quadro! Eu não preciso de mais problemas de 'P vs NP' agora, eu preciso é me formar!"},
            {"speaker": "Mago Místico", "text": "Sua busca por um 'diploma' é um algoritmo com variáveis não definidas. Uma função sem domínio. Uma hipótese sem prova. Você não pode escapar da Estrutura Fundamental."},
            {"speaker": "Player", "text": "Eu posso, sim! Eu vou mostrar que nem toda a matemática discreta do mundo pode me parar quando eu estou motivado para conseguir meu emprego! Meus professores nunca me prepararam para lutar contra um mago da matemática!"},
            {"speaker": "Mago Místico", "text": "Sua motivação é um conjunto vazio. Sua determinação, uma matriz nula. Eu sou a complexidade que você evita, o paradoxo que você não resolve. Você será apenas mais uma variável em minha equação da eternidade!"},
            {"speaker": "Player", "text": "Ah é? Então prepare-se para ser a variável 'x' que eu vou isolar e eliminar! Vamos ver quem resolve quem aqui!"},
            {"speaker": "SYSTEM", "text": "Início da batalha contra o Chefe da Matemática Discreta!"}
        ],
    },
    "FinalBoss": {
        "nome": "Robô Robust Python",
        "bg_image": "imagens_game/data_center_python.png",
        "sprite_enemy": "imagens_boss/robo_python.png",
        "sprite_hero": "imagens_heroi/hero_parado.png",
        "stats": (300, 40, 30, 8, 0),
        "dialogue": [
            {"speaker": "Robô Robust Python", "text": "print(\"Intruso detectado. Inicializando protocolo de eliminação.\")"},
            {"speaker": "Player", "text": "Então você é o chefão, hein? O grande 'Boss Final'! O gênio da programação que está por trás de toda essa bagunça!"},
            {"speaker": "Robô Robust Python", "text": "Error: Argumento inválido. Não sou \"chefão\". Sou a Arquitetura Principal. O Kernel. O Coração da Lógica. Você é apenas um script com erros de sintaxe."},
            {"speaker": "Player", "text": "Um script com erros? Eu sou o aluno que vai te desinstalar! Você transformou minha faculdade em um jogo de terror e impediu minha formatura! Isso não é legal, cara!"},
            {"speaker": "Robô Robust Python", "text": "Ação ilegal. Este é um ambiente controlado. Seu objetivo \"formatura\" é uma variável booleana falsa. Sua presença causa conflito de recursos."},
            {"speaker": "Player", "text": "Eu não sou um conflito de recursos! Eu sou o resolvedor de problemas! Você acha que é invencível só porque sabe um monte de código, mas eu sei que todo sistema tem uma falha!"},
            {"speaker": "Robô Robust Python", "text": "Meus algoritmos são otimizados. Minha lógica é impecável. Minha execução é eficiente. Você não possui as bibliotecas necessárias para me derrotar."},
            {"speaker": "Player", "text": "Pode ser que eu não tenha todas as bibliotecas, mas eu tenho a determinação de um estudante que não quer ser jubilado! E um TCC para defender! Prepare-se para um bug que você não vai conseguir debugar!"},
            {"speaker": "Robô Robust Python", "text": "Warning: Nível de ameaça elevado. Iniciando sequência de defesa. Seus comandos serão ignorados. Sua existência será terminada. Import 'derrota' as 'sua_derrota'."},
            {"speaker": "Player", "text": "Vamos ver quem importa quem aqui! Prepare-se para um traceback que você nunca vai esquecer! Hora de fechar esse portal e mandar você de volta para o else do universo!"},
            {"speaker": "SYSTEM", "text": "Início da batalha final contra o Robô Robust Python!"}
        ],
    },
}