"""Módulo do Teste do Qui-Quadrado (χ²) baseado em Pares de Valores (PoVs)."""

import numpy as np
from scipy.stats import chi2


def calcular_povs(amostras: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Retorna as frequências dos valores pares (2k) e ímpares (2k+1) do histograma."""
    hist = np.bincount(amostras.ravel().astype(np.uint8), minlength=256).astype(np.float64)
    pares = hist[0::2]   # h_{2k}
    impares = hist[1::2] # h_{2k+1}
    return pares, impares


def teste_chi_quadrado(amostras: np.ndarray) -> tuple[float, float]:
    """
    Calcula a estatística Qui-Quadrado (χ²) e a probabilidade de infecção (p-valor).
    Sob H0 (presença de LSB uniforme), o valor esperado de cada par é Z_k = (h_{2k} + h_{2k+1}) / 2.
    """
    pares, impares = calcular_povs(amostras)
    esperado = (pares + impares) / 2.0

    # Filtra apenas pares com frequência esperada suficiente (Z_k >= 1)
    ativos = esperado >= 1.0
    k = int(np.sum(ativos))
    if k <= 1:
        return 0.0, 0.0

    chi2_stat = float(np.sum(((pares[ativos] - esperado[ativos]) ** 2) / esperado[ativos]))
    graus_liberdade = k - 1
    p_valor = float(chi2.sf(chi2_stat, graus_liberdade))
    return chi2_stat, p_valor


def varredura_cumulativa(imagem: np.ndarray, passos: int = 10) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Analisa a imagem em amostras cumulativas (ex.: 10%, 20%, ..., 100% dos pixels).
    Retorna (percentuais, estatisticas_chi2, p_valores).
    """
    pixels = imagem.ravel()
    total = len(pixels)
    fracoes = np.linspace(1.0 / passos, 1.0, passos)

    chi2_lista = []
    p_lista = []

    for frac in fracoes:
        limite = max(2, int(frac * total))
        stat, p_val = teste_chi_quadrado(pixels[:limite])
        chi2_lista.append(stat)
        p_lista.append(p_val)

    return fracoes * 100.0, np.array(chi2_lista), np.array(p_lista)

