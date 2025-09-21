# -*- coding: utf-8 -*-
"""
DASA - Demonstração de Estruturas de Dados em Python
----------------------------------------------------
Contexto: consumo diário de insumos (reagentes e descartáveis) em unidades de diagnóstico.
Objetivo: organizar e consultar esses dados com estruturas clássicas (fila, pilha),
buscas (sequencial e binária) e ordenações (Merge Sort e Quick Sort).

OBS: Este módulo é 100% em memória (sem banco de dados) e focado em demonstrar os conceitos.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque
from typing import List, Optional, Callable, Any, Tuple
import random
import sys

# ---------------------------
# Modelo de domínio (DTO)
# ---------------------------

@dataclass(frozen=True)
class Insumo:
    insumo: str
    quantidade: int
    exame: str
    validade: Optional[datetime] = None


# ---------------------------
# Dados simulados
# ---------------------------

EXAMES = [
    "Hemograma completo",
    "Cultura microbiológica",
    "Glicemia em jejum",
    "PCR",
    "Sorologia (HIV)",
]

INSUMOS = [
    "Agulha 25x7",
    "Swab estéril",
    "Seringa 5ml",
    "Tubo EDTA 4ml",
    "Luva nitrílica M",
    "Luva nitrílica G",
    "Tubo Citrato 3,2%",
]


def gerar_lote_insumos(qtd: int, seed: int = 42) -> List[Insumo]:
    """esta parte ira criar uma lista de insumos com quantidades e validades aleatórias para testes."""
    random.seed(seed)
    hoje = datetime.today()
    itens: List[Insumo] = []
    for _ in range(qtd):
        nome = random.choice(INSUMOS)
        exame = random.choice(EXAMES)
        quantidade = random.randint(1, 200)
        validade = hoje + timedelta(days=random.randint(0, 365))
        itens.append(Insumo(insumo=nome, quantidade=quantidade, exame=exame, validade=validade))
    return itens


# ---------------------------
# Fila e Pilha
# ---------------------------

class FilaConsumo:
    """Cria fila (ordem cronológica) para registrar consumos diários."""
    def __init__(self) -> None:
        self._q = deque()  # cada item será (timestamp, Insumo)

    def registrar_consumo(self, item: Insumo) -> None:
        self._q.append((datetime.now(), item))

    def proximo(self) -> Optional[Tuple[datetime, Insumo]]:
        return self._q.popleft() if self._q else None

    def __len__(self) -> int:
        return len(self._q)

    def __iter__(self):
        return iter(self._q)


class PilhaConsultas:
    """Cria pilha para simular consultas em ordem inversa (LIFO)."""
    def __init__(self) -> None:
        self._stack: List[Tuple[datetime, Insumo]] = []

    def consultar(self, item: Insumo) -> None:
        self._stack.append((datetime.now(), item))

    def ultimo(self) -> Optional[Tuple[datetime, Insumo]]:
        return self._stack.pop() if self._stack else None

    def __len__(self) -> int:
        return len(self._stack)

    def __iter__(self):
        return iter(self._stack)


# ---------------------------
# Buscas
# ---------------------------

def busca_sequencial(insumos: List[Insumo], nome: str) -> Optional[Insumo]:
    """Cria uma busca linear por nome do insumo."""
    for item in insumos:
        if item.insumo.lower() == nome.lower():
            return item
    return None


def busca_binaria(insumos_ordenados: List[Insumo], nome: str) -> Optional[Insumo]:
    """Cria uma busca binária por nome. A lista deve estar ORDENADA por 'insumo'."""
    lo, hi = 0, len(insumos_ordenados) - 1
    nome = nome.lower()
    while lo <= hi:
        mid = (lo + hi) // 2
        atual = insumos_ordenados[mid].insumo.lower()
        if atual == nome:
            return insumos_ordenados[mid]
        if atual < nome:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


def merge_sort(itens: List[Insumo], key: Callable[[Insumo], Any]) -> List[Insumo]:
    """Merge Sort estável; retorna nova lista ordenada pela chave 'key'."""
    if len(itens) <= 1:
        return itens[:]
    mid = len(itens) // 2
    esquerda = merge_sort(itens[:mid], key)
    direita = merge_sort(itens[mid:], key)
    return _merge(esquerda, direita, key)


def _merge(a: List[Insumo], b: List[Insumo], key: Callable[[Insumo], Any]) -> List[Insumo]:
    i = j = 0
    out: List[Insumo] = []
    while i < len(a) and j < len(b):
        if key(a[i]) <= key(b[j]):
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out


def quick_sort(itens: List[Insumo], key: Callable[[Insumo], Any]) -> List[Insumo]:
    """Quick Sort; retorna nova lista ordenada pela chave 'key'."""
    if len(itens) <= 1:
        return itens[:]
    pivot = key(random.choice(itens))
    menores = [x for x in itens if key(x) < pivot]
    iguais  = [x for x in itens if key(x) == pivot]
    maiores = [x for x in itens if key(x) > pivot]
    return quick_sort(menores, key) + iguais + quick_sort(maiores, key)




def _print_insumo(i: Insumo) -> str:
    val = i.validade.strftime("%Y-%m-%d") if i.validade else "—"
    return f"{i.insumo:18}  qtd={i.quantidade:3}  exame={i.exame:24}  validade={val}"




def demo() -> None:
    print("=== DASA • Demonstração de Estruturas de Dados (Python) ===")
    base = gerar_lote_insumos(12)

    print("\nAmostra de dados (não ordenados):")
    for i in base[:6]:
        print("  ", _print_insumo(i))

    # Fila
    fila = FilaConsumo()
    for i in base[:5]:
        fila.registrar_consumo(i)
    print(f"\nFila de consumo registrada ({len(fila)} entradas):")
    for ts, item in fila:
        print("  ", ts.strftime("%H:%M:%S"), "->", item.insumo)

    # Pilha
    pilha = PilhaConsultas()
    for i in base[:5]:
        pilha.consultar(i)
    print(f"\nPilha de consultas registrada ({len(pilha)} entradas):")
    for ts, item in pilha:
        print("  ", ts.strftime("%H:%M:%S"), "->", item.insumo)

    # Buscas
    alvo = base[0].insumo
    achado_seq = busca_sequencial(base, alvo)
    print(f"\nBusca sequencial por '{alvo}':", _print_insumo(achado_seq) if achado_seq else "não encontrado")

    ordenados_nome = merge_sort(base, key=lambda x: x.insumo.lower())
    achado_bin = busca_binaria(ordenados_nome, alvo)
    print(f"Busca binária por '{alvo}':", _print_insumo(achado_bin) if achado_bin else "não encontrado")

    # Ordenações
    por_qtd = merge_sort(base, key=lambda x: x.quantidade)
    print("\nTop 5 menores quantidades (Merge Sort):")
    for i in por_qtd[:5]:
        print("  ", _print_insumo(i))

    por_validade = quick_sort([i for i in base if i.validade], key=lambda x: x.validade)
    print("\nTop 5 validades mais próximas (Quick Sort):")
    for i in por_validade[:5]:
        print("  ", _print_insumo(i))

    print("\nFim da demonstração.\n")


def main() -> None:
    
    print("DASA • Estruturas de Dados (Python)")
    print("1) Rodar demonstração completa")
    print("2) Sair")
    op = input("Escolha uma opção: ").strip()
    if op == "1":
        demo()
    else:
        print("Encerrado.")


if __name__ == "__main__":
    # Você pode chamar diretamente demo() ou usar o menu:
    # demo()
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        sys.exit(0)
