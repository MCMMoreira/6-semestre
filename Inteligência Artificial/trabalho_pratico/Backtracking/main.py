import math
import sys
from sudoku import imprimir_tabuleiro, resolver_sudoku


def carregar_tabuleiro(caminho_arquivo):
    with open(caminho_arquivo, "r") as f:
        linhas_arquivo = f.read().splitlines()

    # Filtra linhas vazias
    linhas_arquivo = [l.strip() for l in linhas_arquivo if l.strip()]

    dimensoes = linhas_arquivo[0].split()
    linhas = int(dimensoes[0])
    colunas = int(dimensoes[1])

    if linhas != colunas:
        raise ValueError("O Sudoku deve ser uma matriz quadrada!")

    tabuleiro = []
    for linha in linhas_arquivo[1 : linhas + 1]:
    
        valores = [int(x) for x in linha.split()]
        
        # Garante que a linha lida tem o tamanho correto
        if len(valores) != colunas:
            raise ValueError(f"A linha '{linha}' não tem {colunas} elementos!")
            
        tabuleiro.append(valores)

    return tabuleiro, linhas


def main():
    # Verifica se o usuário passou o arquivo por argumento
    if len(sys.argv) < 2:
        print(f"Uso correto: python3 {sys.argv[0]} <arquivo_de_entrada.txt>")
        return

    caminho_arquivo = sys.argv[1]

    try:
        tabuleiro, n = carregar_tabuleiro(caminho_arquivo)

        # Calcula dinamicamente o tamanho das subgrades
        tam_bloco = int(math.sqrt(n))

        if tam_bloco * tam_bloco != n:
            print(
                "Aviso: O tamanho da matriz não possui uma raiz quadrada"
            )

        print("SUDOKU INICIAL:\n")
        imprimir_tabuleiro(tabuleiro, n, tam_bloco)

        if resolver_sudoku(tabuleiro, n, tam_bloco):
            print("\nSUDOKU RESOLVIDO:\n")
            imprimir_tabuleiro(tabuleiro, n, tam_bloco)
        else:
            print("\nNão existe solução para este tabuleiro.")

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")


if __name__ == "__main__":
    main()