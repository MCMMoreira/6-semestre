import math
import sys
import contextlib
import time
import copy
from pathlib import Path
from Backtracking.sudoku import resolver_sudoku
from Memetico.memetico import algoritmo_genetico
from generator import gerar_sudokus
from generator import QTD_FACIL,QTD_MEDIO,QTD_DIFICIL

NUM_TESTES = QTD_FACIL + QTD_MEDIO + QTD_DIFICIL


def carregar_tabuleiro(caminho_arquivo):
    """Lê o arquivo de entrada"""
    with open(caminho_arquivo, "r") as f:
        linhas_arquivo = f.read().splitlines()

    # Filtra linhas vazias
    linhas_arquivo = [l.strip() for l in linhas_arquivo if l.strip()]

    if not linhas_arquivo:
        raise ValueError(f"O arquivo {caminho_arquivo} está vazio.")

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


def salvar(arquivo, tabuleiro, n, tam_bloco):
    """Escreve o tabuleiro formatado com as divisórias dentro do arquivo txt"""
    for i in range(n):
        if i % tam_bloco == 0 and i != 0:
            # Linha divisória de blocos horizontais
            arquivo.write("-" * (n * 2 + tam_bloco * 2 - 1) + "\n")

        for j in range(n):
            if j % tam_bloco == 0 and j != 0:
                arquivo.write("| ")
            arquivo.write(f"{tabuleiro[i][j]:2} ")
        arquivo.write("\n")
    arquivo.write("\n")


def main():
    gerar_sudokus()

    f_base = "test/test_files/tab_"

    res_back = Path("test/resultados") / "backtracking.txt"
    res_gen = Path("test/resultados") / "alg_genetico.txt"

    # Garante que a pasta resultados exista
    res_back.parent.mkdir(parents=True, exist_ok=True)

    # Inicializa/Limpa os arquivos de texto principais
    with open(res_back, "w", encoding="utf-8") as arquivo:
        arquivo.write("RESOLUÇÕES - BACKTRACKING\n" + "="*30 + "\n")

    with open(res_gen, "w", encoding="utf-8") as arquivo:
        arquivo.write("RESOLUÇÕES - ALGORITMO GENÉTICO\n" + "="*30 + "\n")

    tempos_genetico = []
    tempos_backtracking = []

    try:

        print("Iniciando Testes com Algoritmo Genético...")
        for i in range(NUM_TESTES):
            caminho_arquivo = f_base + str(i+1) + ".txt"
            
            try:
                tabuleiro, n = carregar_tabuleiro(caminho_arquivo)
            except FileNotFoundError:
                print(f"Aviso: Arquivo {caminho_arquivo} não encontrado. Pulando...")
                continue

            tam_bloco = int(math.sqrt(n))

            with open(res_gen, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"\nTeste {i+1}\n" + "-"*15 + "\n")

            # Cronometra a execução
            inicio = time.time()
            with open('/dev/null', 'w') as devnull:  
                with contextlib.redirect_stdout(devnull):
                    resultado_gen = algoritmo_genetico(copy.deepcopy(tabuleiro))
            fim = time.time()
            
            tempo_decorrido = fim - inicio
            tempos_genetico.append(tempo_decorrido)

            with open(res_gen, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"Tempo de Execução: {tempo_decorrido:.4f} segundos\n")
                arquivo.write("Tabuleiro Resultante:\n")
                # Salva a matriz gerada pelo algoritmo genético (mesmo se contiver conflitos)
                salvar(arquivo, resultado_gen, n, tam_bloco)
            
            print(f"Genético - Tabuleiro {i+1}: {tempo_decorrido:.4f}s")

        print("\nIniciando Testes com Backtracking...")
        for i in range(NUM_TESTES):
            if i < QTD_FACIL:
                label = "Facil"
            elif (i >= QTD_FACIL) and (i <QTD_FACIL+QTD_MEDIO):
                label = "Medio"
            else:
                label = "Dificil"

            caminho_arquivo = f_base + str(i+1) + ".txt"
            
            try:
                tabuleiro, n = carregar_tabuleiro(caminho_arquivo)
            except FileNotFoundError:
                continue

            tam_bloco = int(math.sqrt(n))

            with open(res_back, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"\nTeste {i+1}\n" + "-"*15 + "\n")

            # Cronometra a execução
            inicio = time.time()
            resolvido = resolver_sudoku(tabuleiro, n, tam_bloco)
            fim = time.time()
            
            tempo_decorrido = fim - inicio
            tempos_backtracking.append(tempo_decorrido)

            with open(res_back, "a", encoding="utf-8") as arquivo:
                if resolvido:
                    arquivo.write("Resultado: Resolvido com Sucesso\n")
                    arquivo.write(f"Tempo de Execução: {tempo_decorrido:.4f} segundos\n")
                    arquivo.write("Tabuleiro Resolvido:\n")
                    salvar(arquivo, tabuleiro, n, tam_bloco)
                else:
                    arquivo.write("Resultado: Não possui solução\n")
                    arquivo.write(f"Tempo de Execução: {tempo_decorrido:.4f} segundos\n\n")
            
            print(f"Backtracking - Tabuleiro {label} {i+1}: {tempo_decorrido:.4f}s")

  
        print("\n" + "="*40)
        print("MÉDIAS DE TEMPO DE EXECUÇÃO:")
        print("="*40)
        
        if tempos_genetico:
            media_gen = sum(tempos_genetico) / len(tempos_genetico)
            print(f"Algoritmo Genético: {media_gen:.4f} segundos (Média de {len(tempos_genetico)} testes)")
            with open(res_gen, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"\n{'='*30}\nMÉDIA TOTAL: {media_gen:.4f} segundos\n")
        
        if tempos_backtracking:
            media_back = sum(tempos_backtracking) / len(tempos_backtracking)
            print(f"Backtracking:       {media_back:.4f} segundos (Média de {len(tempos_backtracking)} testes)")
            with open(res_back, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"\n{'='*30}\nMÉDIA TOTAL: {media_back:.4f} segundos\n")

    except Exception as e:
        print(f"Erro inesperado ao processar o arquivo: {e}")


if __name__ == "__main__":
    main()