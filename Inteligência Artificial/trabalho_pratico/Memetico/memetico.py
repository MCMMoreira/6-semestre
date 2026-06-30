import random
import copy

TAMANHO_POPULACAO = 200  # Quantidade de tabuleiros por geração
GERACOES = 500  # Limite máximo de iterações do algoritmo
TAXA_MUTACAO = 0.02  # 2% de chance de sofrer mutação por linha
ELITISMO = 10  # Quantidade de melhores indivíduos que passam direto
ESTAGNACAO_MAX = 15  # Gerações sem melhora antes de resetar a população
BUSCA_LOCAL_ITER = 100  # Tentativas de melhoria por busca local


def obter_posicoes_fixas(tabuleiro):
    fixas = set()
    n = len(tabuleiro)
    for i in range(n):
        for j in range(n):
            if tabuleiro[i][j] != 0:
                fixas.add((i, j))
    return fixas


def criar_individuo(tabuleiro_inicial, fixas):
    individuo = copy.deepcopy(tabuleiro_inicial) #faz uma copia do tabuleiro inicial
    n = len(individuo)
    for linha in range(n):
        existentes = {v for v in individuo[linha] if v != 0}
        faltantes = [v for v in range(1, n + 1) if v not in existentes] #lista os numeros que estao faltando na linha
        random.shuffle(faltantes) #embaralha os numeros
        indice = 0
        for coluna in range(n):
            if individuo[linha][coluna] == 0: #completa as lacunas
                individuo[linha][coluna] = faltantes[indice]
                indice += 1
    busca_local(individuo, fixas) #otimiza o individuo que acabou de ser criado
    return individuo #retorna o tabuleiro preenchido


def criar_populacao(tabuleiro, fixas, tamanho):
    return [criar_individuo(tabuleiro, fixas) for _ in range(tamanho)] #cria uma lista de individuos


def fitness(individuo):

    n = len(individuo)
    bloco = int(n ** 0.5)
    conflitos = 0

    # conta conflitos nas colunas
    for coluna in range(n):
        valores = [individuo[linha][coluna] for linha in range(n)]
        conflitos += n - len(set(valores))

    # Validação por blocos
    for bl in range(bloco):  # Varre os blocos na vertical
        for bc in range(bloco):  # Varre os blocos na horizontal
            valores = []  # Lista para armazenar valores do bloco atual
            for i in range(bl * bloco, bl * bloco + bloco):  # Linhas do bloco
                for j in range(
                    bc * bloco, bc * bloco + bloco
                ):  # Colunas do bloco
                    valores.append(individuo[i][j])  # Coleta o número
            conflitos += n - len(set(valores))  # Adiciona duplicatas do bloco

    return conflitos


def busca_local(individuo, fixas):
    n = len(individuo)
    fit_atual = fitness(individuo)

    for _ in range(BUSCA_LOCAL_ITER):
        linha = random.randint(0, n - 1) #escolhe uma linha aleatória
        livres = [c for c in range(n) if (linha, c) not in fixas] #filtra as colunas que não são fixas
        if len(livres) < 2:
            continue

        # Escolhe duas colunas livre e inverte os valores das duas colunas escolhidas 
        c1, c2 = random.sample(livres, 2)
        individuo[linha][c1], individuo[linha][c2] = (
            individuo[linha][c2],
            individuo[linha][c1],
        )
        fit_novo = fitness(individuo) #avalia o novo fitness

        if fit_novo <= fit_atual:
            fit_atual = fit_novo #se melhorou ou manteve, substitui
        else: #se não, desfaz
            individuo[linha][c1], individuo[linha][c2] = (
                individuo[linha][c2],
                individuo[linha][c1],
            )

    return fit_atual


def selecao_torneio(populacao, fitnesses, k=5):
    indices = random.sample(range(len(populacao)), k) #sorteia k competidores
    melhor_idx = min(indices, key=lambda i: fitnesses[i]) # encontra o indice do competidor com menor fitness
    return copy.deepcopy(populacao[melhor_idx]) #retorna copia do vencedor


def crossover(pai1, pai2): #herda metade do tabuleiro de um pai, e a outra metado do outro
    n = len(pai1)
    ponto = random.randint(1, n - 1)
    filho = []
    for i in range(n):
        if i < ponto:
            filho.append(pai1[i][:])
        else:
            filho.append(pai2[i][:])
    return filho


# para cada linha, sorteia duas colunas aleatorias e troca
def mutacao(individuo, fixas):
    n = len(individuo)
    for linha in range(n):
        if random.random() < TAXA_MUTACAO:
            livres = [c for c in range(n) if (linha, c) not in fixas]
            if len(livres) >= 2:
                c1, c2 = random.sample(livres, 2)
                individuo[linha][c1], individuo[linha][c2] = (
                    individuo[linha][c2],
                    individuo[linha][c1],
                )


def algoritmo_genetico(tabuleiro_inicial):
    fixas = obter_posicoes_fixas(tabuleiro_inicial) #pega as dicas iniciais que não podem ser alteradas
    populacao = criar_populacao(tabuleiro_inicial, fixas, TAMANHO_POPULACAO)

    melhor = None # Variável para armazenar a melhor solução do histórico
    melhor_fitness_global = float("inf") # Começa com a pior pontuação possível
    geracoes_sem_melhora = 0 # Contador de estagnação

    for geracao in range(GERACOES):
        fitnesses = [fitness(ind) for ind in populacao] # Avalia todos os indivíduos

        # Identifica o melhor indivíduo da geração atual
        melhor_idx = min(range(len(populacao)), key=lambda i: fitnesses[i])
        melhor_fitness = fitnesses[melhor_idx]
        melhor = copy.deepcopy(populacao[melhor_idx])

        print(f"Geração {geracao} - Fitness = {melhor_fitness}")

        if melhor_fitness == 0: #solução perfeita
            print("\nSolução encontrada!")
            return melhor

        if melhor_fitness < melhor_fitness_global: #se houve melhora
            melhor_fitness_global = melhor_fitness #atualiza o melhor
            geracoes_sem_melhora = 0 #reseta o contador de estagnação
        else:
            geracoes_sem_melhora += 1 #incrementa o contador de estagnação

        # Reinicialização por estagnação, preservando elites
        if geracoes_sem_melhora >= ESTAGNACAO_MAX:
            print(f"  Estagnação — reinicializando...")
            indices_ord = sorted(range(len(populacao)), key=lambda i: fitnesses[i]) # Ordena a população pelos melhores índices (menor fitness)
            elites = [copy.deepcopy(populacao[i]) for i in indices_ord[:ELITISMO]] # Salva os melhores
            nova = criar_populacao(tabuleiro_inicial, fixas, TAMANHO_POPULACAO - ELITISMO) # Cria novos indivíduos para preencher as vagas restantes
            populacao = elites + nova #junta os individuos
            geracoes_sem_melhora = 0
            continue

        # criacao da nova populacao convencional
        indices_ord = sorted(range(len(populacao)), key=lambda i: fitnesses[i]) # Preserva os melhores indivíduos
        nova_populacao = [copy.deepcopy(populacao[i]) for i in indices_ord[:ELITISMO]]

        #loop da reproducao
        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1 = selecao_torneio(populacao, fitnesses) #seleciona o pai1 
            pai2 = selecao_torneio(populacao, fitnesses) # seleciona o pai 2
            filho = crossover(pai1, pai2) #faz o cruzamento
            mutacao(filho, fixas) #aplica mutação
            # Busca local após crossover+mutação 
            busca_local(filho, fixas)
            nova_populacao.append(filho) #insere o filho na nova populaçao

        populacao = nova_populacao #substitui a antiga pela nova

    return melhor
