"""Funções auxiliares para geração de imagem de teste, execução do experimento e gráficos."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

from lsb import inserir_lsb_sequencial, inserir_lsb_pseudoaleatorio
from chi_square import varredura_cumulativa


def gerar_imagem_padrao(altura: int = 512, largura: int = 512, seed: int = 2026) -> np.ndarray:
    """Gera uma imagem sintética em tons de cinza com estruturas e assimetria natural entre PoVs."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:altura, 0:largura].astype(np.float64)
    yn, xn = y / altura, x / largura

    cena = (
        100.0
        + 50.0 * np.sin(2.0 * np.pi * (1.5 * xn + 0.8 * yn))
        + 35.0 * np.cos(2.0 * np.pi * (3.0 * yn - 1.5 * xn))
    )
    textura = gaussian_filter(rng.normal(0.0, 25.0, size=(altura, largura)), sigma=3.0)
    bruto = np.clip(np.round(cena + textura), 0, 255).astype(np.int32)

    # Assimetria natural entre intensidades pares e ímpares (típica de sensores reais)
    vies = ((bruto % 2 == 1) & ((x.astype(np.int32) + y.astype(np.int32)) % 4 != 0)).astype(np.int32)
    return np.clip(bruto - vies, 0, 255).astype(np.uint8)


def rodar_bateria_testes(imagem_limpa: np.ndarray, passos: int = 10) -> dict:
    """
    Gera as versões esteganografadas (LSB Sequencial e Pseudoaleatório em 10%, 50%, 100%)
    e aplica a varredura do Qui-Quadrado em todas elas.
    """
    casos = {
        "Limpa (0%)": imagem_limpa,
        "LSB Sequencial (10%)": inserir_lsb_sequencial(imagem_limpa, 0.10, seed=10),
        "LSB Sequencial (50%)": inserir_lsb_sequencial(imagem_limpa, 0.50, seed=50),
        "LSB Sequencial (100%)": inserir_lsb_sequencial(imagem_limpa, 1.00, seed=100),
        "LSB Pseudoaleatório (10%)": inserir_lsb_pseudoaleatorio(imagem_limpa, 0.10, seed=10),
        "LSB Pseudoaleatório (50%)": inserir_lsb_pseudoaleatorio(imagem_limpa, 0.50, seed=50),
        "LSB Pseudoaleatório (100%)": inserir_lsb_pseudoaleatorio(imagem_limpa, 1.00, seed=100),
    }

    resultados = {}
    for nome, img in casos.items():
        pcts, chi2_vals, p_vals = varredura_cumulativa(img, passos=passos)
        resultados[nome] = {
            "imagem": img,
            "percentuais": pcts,
            "chi2": chi2_vals,
            "p_valores": p_vals,
        }

    return resultados


def plotar_comparativo(resultados: dict) -> plt.Figure:
    """Gera a figura comparando LSB Sequencial e LSB Pseudoaleatório ao longo da varredura."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)

    # Gráfico 1: LSB Sequencial
    for nome, cor, marcador in [
        ("Limpa (0%)", "#2ca02c", "o"),
        ("LSB Sequencial (10%)", "#ff7f0e", "s"),
        ("LSB Sequencial (50%)", "#1f77b4", "^"),
        ("LSB Sequencial (100%)", "#d62728", "D"),
    ]:
        dados = resultados[nome]
        ax1.plot(dados["percentuais"], dados["p_valores"], marker=marcador, color=cor, linewidth=2, label=nome)

    ax1.set_title("LSB Sequencial vs. Imagem Limpa")
    ax1.set_xlabel("Percentual da Imagem Analisada (%)")
    ax1.set_ylabel("Probabilidade de Detecção (p-valor)")
    ax1.set_ylim(-0.05, 1.05)
    ax1.grid(True, linestyle="--", alpha=0.4)
    ax1.legend()

    # Gráfico 2: LSB Pseudoaleatório
    for nome, cor, marcador in [
        ("Limpa (0%)", "#2ca02c", "o"),
        ("LSB Pseudoaleatório (10%)", "#ff7f0e", "s"),
        ("LSB Pseudoaleatório (50%)", "#1f77b4", "^"),
        ("LSB Pseudoaleatório (100%)", "#d62728", "D"),
    ]:
        dados = resultados[nome]
        ax2.plot(dados["percentuais"], dados["p_valores"], marker=marcador, linestyle="--", color=cor, linewidth=2, label=nome)

    ax2.set_title("LSB Pseudoaleatório vs. Imagem Limpa")
    ax2.set_xlabel("Percentual da Imagem Analisada (%)")
    ax2.set_ylim(-0.05, 1.05)
    ax2.grid(True, linestyle="--", alpha=0.4)
    ax2.legend()

    fig.tight_layout()
    return fig

