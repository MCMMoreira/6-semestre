import random
import math
import copy
from pathlib import Path

TAMANHO = 9

# Quantidade de tabuleiros a serem gerados para cada nível
QTD_FACIL = 5
QTD_MEDIO = 5
QTD_DIFICIL = 5

# Porcentagem de células que devem vir preenchidas no tabuleiro inicial
PORCENTAGEM_FACIL = 0.45   
PORCENTAGEM_MEDIO = 0.30    
PORCENTAGEM_DIFICIL = 0.15


def eh_valido(tabuleiro, num, pos):
    linha, coluna = pos #posicao da celula a ser verificada
    tam_bloco = int(math.sqrt(TAMANHO)) #tamanho do quadrante
    
    # Valida linha
    for j in range(TAMANHO):
        if tabuleiro[linha][j] == num and j != coluna:
            return False
            
    # Valida coluna
    for i in range(TAMANHO):
        if tabuleiro[i][coluna] == num and i != linha:
            return False
            
    # Valida bloco
    ini_linha = (linha // tam_bloco) * tam_bloco 
    ini_coluna = (coluna // tam_bloco) * tam_bloco
    for i in range(ini_linha, ini_linha + tam_bloco):
        for j in range(ini_coluna, ini_coluna + tam_bloco):
            if tabuleiro[i][j] == num and (i, j) != pos:
                return False
                
    return True

def resolver_e_preencher(tabuleiro):
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            if tabuleiro[i][j] == 0:
                numeros = list(range(1, TAMANHO + 1)) #cria uma lista de números de 1 até tamanho
                random.shuffle(numeros)  # Embaralha para gerar tabuleiros diferentes
                
                for num in numeros:
                    if eh_valido(tabuleiro, num, (i, j)): 
                        tabuleiro[i][j] = num 
                        if resolver_e_preencher(tabuleiro): # testa a hipótese de preencher a celula com o numero
                            return True
                        tabuleiro[i][j] = 0 # testa a hipótese de não preencher
                return False
    return True

def gerar_tabuleiro_completo():
    tabuleiro = [[0] * TAMANHO for _ in range(TAMANHO)] #cria um tabuleiro zerado
    resolver_e_preencher(tabuleiro) #preenche pra garantir que é resolvível
    return tabuleiro

def esvaziar_tabuleiro(tabuleiro_completo, porcentagem_preenchimento):

    tabuleiro_esvaziado = copy.deepcopy(tabuleiro_completo) #cria uma copia do tabuleiro completo
    total_celulas = TAMANHO * TAMANHO
    celulas_a_manter = int(total_celulas * porcentagem_preenchimento)
    celulas_a_remover = total_celulas - celulas_a_manter # calcula quantidade de celulas a serem "apagadas"
    
    posicoes = [(i, j) for i in range(TAMANHO) for j in range(TAMANHO)] # contem todos os indices de posição
    random.shuffle(posicoes) # embaralha os indices
    
    for k in range(celulas_a_remover):
        i, j = posicoes[k]
        tabuleiro_esvaziado[i][j] = 0 #pega os indices na ordem embaralhada, e substitui os k primeiros por 0
        
    return tabuleiro_esvaziado

def salvar_txt(tabuleiro, número_arquivo, diretorio_saida):

    diretorio_saida.mkdir(parents=True, exist_ok=True)
    caminho = diretorio_saida / f"tab_{número_arquivo}.txt"
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"{TAMANHO} {TAMANHO}\n")
        for linha in tabuleiro:
            f.write(" ".join(map(str, linha)) + "\n")

def gerar_sudokus():

    diretorio_testes = Path("test/test_files")
    
    configuracoes = [
        (QTD_FACIL, PORCENTAGEM_FACIL, "Fácil"),
        (QTD_MEDIO, PORCENTAGEM_MEDIO, "Médio"),
        (QTD_DIFICIL, PORCENTAGEM_DIFICIL, "Difícil")
    ]
    
    contador_arquivo = 1
    print(f"Gerando tabuleiros {TAMANHO}x{TAMANHO} em '{diretorio_testes}'...")
    
    for qtd, porcentagem, nivel in configuracoes:
        print(f" -> Criando {qtd} tabuleiros nível {nivel} ({int(porcentagem*100)}% preenchido)...")
        for _ in range(qtd):
            gabarito = gerar_tabuleiro_completo() # gera o tabuleiro resolvido
            tabuleiro_jogo = esvaziar_tabuleiro(gabarito, porcentagem) #limpa as celulas para preparar para o jogo
            salvar_txt(tabuleiro_jogo, contador_arquivo, diretorio_testes) # salva o arquivo na pasta correta
            contador_arquivo += 1
            
    print(f"Sucesso! {contador_arquivo - 1} arquivos gerados.")

if __name__ == "__main__":
    gerar_sudokus()