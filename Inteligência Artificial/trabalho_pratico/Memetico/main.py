from memetico import algoritmo_genetico
import sys


def ler_tabuleiro(nome_arquivo):

    with open(nome_arquivo, "r") as arquivo:

        linhas = arquivo.readlines()

    tabuleiro = []

    for linha in linhas[1:]:   # ignora a primeira linha

        linha = linha.strip()

        if linha == "":
            continue

        tabuleiro.append(
            list(map(int, linha.split()))
        )

    return tabuleiro


def imprimir(tabuleiro):

    n = len(tabuleiro)

    bloco = int(n ** 0.5)

    for i in range(n):

        if i != 0 and i % bloco == 0:
            print("-" * (n * 2 + bloco))

        for j in range(n):

            if j != 0 and j % bloco == 0:
                print("|", end=" ")

            print(tabuleiro[i][j], end=" ")

        print()


def main():

    if len(sys.argv) != 2:

        print(
            "Uso: python3 main.py <arquivo>"
        )

        return

    arquivo = sys.argv[1]

    sudoku = ler_tabuleiro(arquivo)

    print("\nSudoku inicial:\n")

    imprimir(sudoku)

    resultado = algoritmo_genetico(sudoku)

    print("\nMelhor solução encontrada:\n")

    imprimir(resultado)


if __name__ == "__main__":
    main()