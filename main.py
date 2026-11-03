"""
Ponto de entrada principal (main) do Projeto 3 — Esteganálise pelo Teste do Qui-Quadrado (χ²).

Como executar:
  - Usando imagem padrão:      .venv/bin/python3 main.py
  - Passando uma imagem:       .venv/bin/python3 main.py caminho/para/imagem.png
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from experimento import gerar_imagem_padrao, rodar_bateria_testes, plotar_comparativo


def carregar_imagem(caminho: str) -> np.ndarray:
    """Lê uma imagem do disco e converte para matriz uint8 em escala de cinza."""
    img = Image.open(caminho).convert("L")
    return np.array(img, dtype=np.uint8)


def main() -> None:
    """Executa o experimento de esteganálise Qui-Quadrado e salva o gráfico."""
    pasta_graficos = Path(__file__).resolve().parent / "graficos"
    pasta_graficos.mkdir(exist_ok=True)

    if len(sys.argv) > 1:
        caminho_img = sys.argv[1]
        print(f"Carregando imagem: {caminho_img}")
        imagem = carregar_imagem(caminho_img)
    else:
        print("Gerando imagem de teste padrão (512x512)...")
        imagem = gerar_imagem_padrao(512, 512)

    resultados = rodar_bateria_testes(imagem, passos=10)

    fig = plotar_comparativo(resultados)
    caminho_saida = pasta_graficos / "comparativo_chi_quadrado.png"
    fig.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print("\n=== TABELA DE P-VALORES (10% a 100% DA IMAGEM) ===")
    cabecalho = f"{'Cenário':<28} | " + " | ".join(f"{p:>5}%" for p in range(10, 101, 10))
    print(cabecalho)
    print("-" * len(cabecalho))
    for nome, dados in resultados.items():
        valores = " | ".join(f"{v:6.4f}" for v in dados["p_valores"])
        print(f"{nome:<28} | {valores}")
    print(f"\nGráfico salvo em: {caminho_saida}")


if __name__ == "__main__":
    main()
