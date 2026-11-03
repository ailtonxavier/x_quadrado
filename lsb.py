"""Módulo de inserção esteganográfica LSB (Sequencial e Pseudoaleatório)."""

import numpy as np


def inserir_lsb_sequencial(imagem: np.ndarray, taxa_payload: float, seed: int = 42) -> np.ndarray:
    """Insere bits aleatórios nos LSBs de forma sequencial (do início ao fim da imagem)."""
    stego = imagem.copy().astype(np.uint8)
    pixels = stego.ravel()
    n_bits = int(len(pixels) * taxa_payload)

    if n_bits > 0:
        rng = np.random.default_rng(seed)
        bits = rng.integers(0, 2, size=n_bits, dtype=np.uint8)
        pixels[:n_bits] = (pixels[:n_bits] & 0xFE) | bits

    return stego


def inserir_lsb_pseudoaleatorio(imagem: np.ndarray, taxa_payload: float, seed: int = 42) -> np.ndarray:
    """Insere bits aleatórios nos LSBs espalhados pseudoaleatoriamente pela imagem."""
    stego = imagem.copy().astype(np.uint8)
    pixels = stego.ravel()
    n_bits = int(len(pixels) * taxa_payload)

    if n_bits > 0:
        rng = np.random.default_rng(seed)
        bits = rng.integers(0, 2, size=n_bits, dtype=np.uint8)
        posicoes = rng.choice(len(pixels), size=n_bits, replace=False)
        pixels[posicoes] = (pixels[posicoes] & 0xFE) | bits

    return stego

