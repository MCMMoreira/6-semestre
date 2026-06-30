import math

def encontrar_vazia(tabuleiro, n):
    """
    Varre o tabuleiro N x N para encontrar a primeira célula com valor 0
    """
    for linha in range(n):
        for coluna in range(n):
            # Se encontrar o valor 0 significa que a célula está vazia
            if tabuleiro[linha][coluna] == 0:
                return (linha, coluna) # Retorna a posição 
    return None # Se sair do loop o Sudoku não tem mais espaços vazios


def eh_valido(tabuleiro, numero, posicao, n, tam_bloco):
    linha, coluna = posicao

    # Percorre todas as colunas da linha atual
    for j in range(n):
        # Se achar o mesmo número em outra coluna, a jogada é inválida
        if tabuleiro[linha][j] == numero and j != coluna:
            return False

    # Percorre todas as linhas da coluna atual
    for i in range(n):
        # Se achar o mesmo número em outra linha, a jogada é inválida
        if tabuleiro[i][coluna] == numero and i != linha:
            return False

    # Descobre os índices do bloco usando divisão 
    bloco_linha = linha // tam_bloco
    bloco_coluna = coluna // tam_bloco

    # Multiplica para achar a coordenada exata onde o bloco começa na matriz
    inicio_linha = bloco_linha * tam_bloco
    inicio_coluna = bloco_coluna * tam_bloco

    # Percorre apenas as linhas e colunas do bloco
    for i in range(inicio_linha, inicio_linha + tam_bloco):
        for j in range(inicio_coluna, inicio_coluna + tam_bloco):
            # Se o número já existir dentro do bloco, a jogada é inválida
            if tabuleiro[i][j] == numero and (i, j) != posicao:
                return False

    # Se passou pelas 3 checagens, o número pode ser inserido 
    return True


def resolver_sudoku(tabuleiro, n, tam_bloco):

    #Seleciona uma variável (célula vazia)
    posicao = encontrar_vazia(tabuleiro, n)

    #Se não houver mais células vazias, o Sudoku foi resolvido 
    if posicao is None:
        return True

    linha, coluna = posicao

    # Tenta atribuir valores do Domínio (de 1 até N) para a célula atual
    for numero in range(1, n + 1):
        # Verifica se o número atende às restrições
        if eh_valido(tabuleiro, numero, (linha, coluna), n, tam_bloco):
            # Faz a atribuição provisória avançando na árvore de busca
            tabuleiro[linha][coluna] = numero

            # Chama a função recursivamente para tentar resolver o resto do tabuleiro
            if resolver_sudoku(tabuleiro, n, tam_bloco):
                return True 

            # Se a escolha desse numero causou um erro mais adiante,
            # desfazemos a escolha limpando a célula e tentamos o próximo número.
            tabuleiro[linha][coluna] = 0

    # Se testou todos os números de 1 a N e nenhum funcionou nesta célula, 
    # avisa a função anterior que este caminho é um beco sem saída
    return False


def imprimir_tabuleiro(tabuleiro, n, tam_bloco):

    for i in range(n):

        if i % tam_bloco == 0 and i != 0:
            # Calcula o tamanho da linha divisória com base no tamanho do tabuleiro
            print("-" * (n * 2 + tam_bloco * 2 - 1))

        for j in range(n):
            # Se mudou de bloco horizontal, imprime uma barra vertical divisória
            if j % tam_bloco == 0 and j != 0:
                print("|", end=" ")
            
            print(f"{tabuleiro[i][j]:2}", end=" ")
        print() # Quebra de linha ao final de cada linha 