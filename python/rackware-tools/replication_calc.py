#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculadora de estimativa de tempo de replicação/migração (inspirada na planilha fastconnect1gb.xlsx).

- Lê parâmetros como tamanho total de dados, largura de banda, overhead, compressão,
  paralelismo e janela diária de execução.
- Calcula throughput efetivo, tempo total e cronograma por janela diária.
- Gera saída em formato tabela (console), CSV, Markdown ou JSON.
- Oferece três cenários: pessimista, realista e otimista.
- Modo simples: use perfis pré-definidos (--perfil) para evitar muitos parâmetros.

Uso rápido:
  python3 replication_calc.py --dados 5TB --banda 1Gbps --perfil fastconnect --janela 8h --cenario realista --saida tabela

Autor: Programador Python
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

# ===============================
# Utilidades de parsing de unidades
# ===============================

SIZE_UNITS = {
    # SI
    "B": 1,
    "KB": 10**3,
    "MB": 10**6,
    "GB": 10**9,
    "TB": 10**12,
    "PB": 10**15,
    # IEC
    "KiB": 2**10,
    "MiB": 2**20,
    "GiB": 2**30,
    "TiB": 2**40,
    "PiB": 2**50,
}

BITRATE_UNITS = {
    # bits por segundo
    "bps": 1,
    "Kbps": 10**3,
    "Mbps": 10**6,
    "Gbps": 10**9,
    "Tbps": 10**12,
}

TIME_UNITS = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
}

DEFAULT_STREAM_EFFICIENCY = 0.6  # eficiência de um único fluxo (fração da capacidade pós-overhead)


def parse_size(value: str) -> int:
    """Converte string como '500GB', '5TiB', '1200 MB' para bytes."""
    s = value.strip().replace(" ", "")
    # separa número e sufixo
    i = 0
    while i < len(s) and (s[i].isdigit() or s[i] in ".,"):
        i += 1
    number = s[:i].replace(",", ".")
    unit = s[i:] or "B"
    if unit not in SIZE_UNITS:
        raise argparse.ArgumentTypeError(f"Unidade de tamanho desconhecida: {unit}")
    try:
        n = float(number)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Valor numérico inválido: {number}")
    return int(n * SIZE_UNITS[unit])


def parse_bitrate(value: str) -> int:
    """Converte string como '1Gbps', '500 Mbps' para bits por segundo."""
    s = value.strip().replace(" ", "")
    i = 0
    while i < len(s) and (s[i].isdigit() or s[i] in ".,"):
        i += 1
    number = s[:i].replace(",", ".")
    unit = s[i:] or "bps"
    if unit not in BITRATE_UNITS:
        raise argparse.ArgumentTypeError(f"Unidade de banda desconhecida: {unit}")
    try:
        n = float(number)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Valor numérico inválido: {number}")
    return int(n * BITRATE_UNITS[unit])


def parse_time_window(value: str) -> int:
    """Converte string como '8h', '12 m', '1.5d' para segundos."""
    s = value.strip().replace(" ", "")
    i = 0
    while i < len(s) and (s[i].isdigit() or s[i] in ".,"):
        i += 1
    number = s[:i].replace(",", ".")
    unit = s[i:] or "s"
    if unit not in TIME_UNITS:
        raise argparse.ArgumentTypeError(f"Unidade de tempo desconhecida: {unit}")
    try:
        n = float(number)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Valor numérico inválido: {number}")
    return int(n * TIME_UNITS[unit])


def parse_percentage(value: str) -> float:
    """Converte '15' ou '15%' em fração (0.15)."""
    s = value.strip().replace(" ", "")
    if s.endswith("%"):
        s = s[:-1]
    try:
        v = float(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Percentual inválido: {value}")
    if v < 0 or v >= 100:
        raise argparse.ArgumentTypeError("Percentual deve estar entre 0 e 100")
    return v / 100.0


# ===============================
# Modelo de Cenário
# ===============================

@dataclass
class Scenario:
    nome: str
    overhead_frac: float       # fração (ex: 0.15 para 15%)
    compressao_frac: float     # fração de redução (ex: 0.3 => reduz 30% do volume)
    eficacia_paralelismo: float  # fração de eficiência de paralelismo (0..1)
    eficiencia_stream: float     # eficiência de um único fluxo (0..1)


# ===============================
# Cálculos centrais
# ===============================

def calcular_volume_pos_compressao(bytes_totais: int, compressao_frac: float) -> int:
    """Aplica redução por compressão. compressao_frac=0.3 => mantém 70% do volume."""
    fator = 1.0 - compressao_frac
    return max(0, int(bytes_totais * fator))


def calcular_throughput_efetivo_bps(
    bps_link: int,
    overhead_frac: float,
    paralelismo: int,
    eficacia_paralelismo: float,
    eficiencia_stream: float = DEFAULT_STREAM_EFFICIENCY,
) -> float:
    """Throughput efetivo com limites físicos do link.
    - Capacidade pós-overhead: cap = bps_link * (1 - overhead)
    - Um único fluxo atinge cap * eficiencia_stream
    - Paralelismo aumenta a taxa: base * (1 + (paralelismo - 1) * eficacia)
    - Resultado é limitado por cap (não pode exceder a capacidade do link)
    """
    cap = bps_link * (1.0 - overhead_frac)
    base = cap * max(0.0, min(1.0, eficiencia_stream))
    if paralelismo <= 1:
        return min(base, cap)
    ganho = 1.0 + (paralelismo - 1) * max(0.0, min(1.0, eficacia_paralelismo))
    return min(base * ganho, cap)


def calcular_duracao_segundos(bytes_totais: int, bps_efetivo: float) -> float:
    """Tempo total em segundos para transferir bytes_totais a bps_efetivo (bits/s)."""
    if bps_efetivo <= 0:
        return math.inf
    # Converter bytes para bits
    bits_totais = bytes_totais * 8.0
    return bits_totais / bps_efetivo


def decompor_tempo(segundos: float) -> Tuple[int, int, int, int]:
    """Decompõe segundos em (dias, horas, minutos, segundos)."""
    if math.isinf(segundos):
        return (math.inf, math.inf, math.inf, math.inf)  # tipo: ignore
    s = int(round(segundos))
    d = s // 86400
    s %= 86400
    h = s // 3600
    s %= 3600
    m = s // 60
    s %= 60
    return d, h, m, s


def estimar_cronograma(duracao_total_s: float, janela_diaria_s: int, disponibilidade_s: int) -> Dict[str, int]:
    """Estima quantos dias de janela serão necessários dado a janela diária e disponibilidade total.
    Retorna dict com dias_totais, janelas_necessarias, sobra_segundos.
    """
    if math.isinf(duracao_total_s):
        return {"janelas_necessarias": math.inf, "dias_totais": math.inf, "sobra_segundos": math.inf}  # type: ignore
    if janela_diaria_s <= 0:
        return {"janelas_necessarias": math.inf, "dias_totais": math.inf, "sobra_segundos": math.inf}  # type: ignore
    janelas = math.ceil(duracao_total_s / janela_diaria_s)
    dias = janelas  # assumindo 1 janela por dia
    sobra = int(janelas * janela_diaria_s - duracao_total_s)
    dentro_disponibilidade = (dias * 86400) <= disponibilidade_s if disponibilidade_s > 0 else True
    return {
        "janelas_necessarias": janelas,
        "dias_totais": dias,
        "sobra_segundos": max(0, sobra),
        "dentro_disponibilidade": 1 if dentro_disponibilidade else 0,
    }


# ===============================
# Saídas formatadas
# ===============================

def formatar_duracao(segundos: float) -> str:
    if math.isinf(segundos):
        return "infinito"
    d, h, m, s = decompor_tempo(segundos)
    return f"{d}d {h}h {m}m {s}s"


def formatar_tabela_resultado(res: Dict[str, object]) -> str:
    linhas = []
    add = linhas.append
    add("================= Estimativa de Migração =================")
    add(f"Cenário: {res['cenario']}")
    add("----------------------------------------------------------")
    add(f"Dados (após compressão): {res['dados_pos_compressao_gb']} GB")
    add(f"Throughput efetivo: {res['throughput_mbps']} Mbps")
    add(f"Duração total: {res['duracao_formatada']}")
    add(f"Janelas necessárias: {res['cronograma']['janelas_necessarias']}")
    add(f"Dias totais (1 janela/dia): {res['cronograma']['dias_totais']}")
    add(f"Sobra por última janela: {formatar_duracao(res['cronograma']['sobra_segundos'])}")
    add(f"Dentro da disponibilidade: {'Sim' if res['cronograma']['dentro_disponibilidade'] else 'Não'}")
    return "\n".join(linhas)


def formatar_csv(res: Dict[str, object]) -> str:
    headers = [
        "cenario", "dados_pos_compressao_gb", "throughput_mbps", "duracao_segundos",
        "janelas_necessarias", "dias_totais", "sobra_segundos", "dentro_disponibilidade"
    ]
    values = [
        res["cenario"],
        res["dados_pos_compressao_gb"],
        res["throughput_mbps"],
        int(res["duracao_segundos"]),
        res["cronograma"]["janelas_necessarias"],
        res["cronograma"]["dias_totais"],
        res["cronograma"]["sobra_segundos"],
        res["cronograma"]["dentro_disponibilidade"],
    ]
    return ",".join(map(str, headers)) + "\n" + ",".join(map(str, values))


def formatar_markdown(res: Dict[str, object]) -> str:
    md = []
    add = md.append
    add("| Campo | Valor |")
    add("|---|---:|")
    add(f"| Cenário | {res['cenario']} |")
    add(f"| Dados (após compressão) | {res['dados_pos_compressao_gb']} GB |")
    add(f"| Throughput efetivo | {res['throughput_mbps']} Mbps |")
    add(f"| Duração total | {res['duracao_formatada']} |")
    add(f"| Janelas necessárias | {res['cronograma']['janelas_necessarias']} |")
    add(f"| Dias totais (1 janela/dia) | {res['cronograma']['dias_totais']} |")
    add(f"| Sobra por última janela | {formatar_duracao(res['cronograma']['sobra_segundos'])} |")
    add(f"| Dentro da disponibilidade | {'Sim' if res['cronograma']['dentro_disponibilidade'] else 'Não'} |")
    return "\n".join(add for add in md)


# ===============================
# Perfis (modo simples)
# ===============================

def perfil_defaults(perfil: str) -> Dict[str, float | int]:
    p = perfil.lower()
    if p == "fastconnect":
        return {"overhead": 0.15, "compressao": 0.30, "eficacia": 0.85, "paralelismo": 4, "eficiencia_stream": 0.6}
    if p == "vpn":
        return {"overhead": 0.25, "compressao": 0.30, "eficacia": 0.70, "paralelismo": 4, "eficiencia_stream": 0.5}
    if p == "internet":
        return {"overhead": 0.20, "compressao": 0.20, "eficacia": 0.60, "paralelismo": 4, "eficiencia_stream": 0.5}
    if p == "lan":
        return {"overhead": 0.10, "compressao": 0.10, "eficacia": 0.90, "paralelismo": 2, "eficiencia_stream": 0.8}
    # padrão conservador
    return {"overhead": 0.20, "compressao": 0.20, "eficacia": 0.60, "paralelismo": 2, "eficiencia_stream": 0.6}


# ===============================
# Execução principal (CLI)
# ===============================

def montar_cenarios(base_overhead: float, base_compressao: float, eficacia_paralelismo: float, eficiencia_stream: float) -> Dict[str, Scenario]:
    """Cria três cenários padrão a partir de parâmetros base."""
    return {
        "pessimista": Scenario("pessimista", overhead_frac=min(0.5, base_overhead + 0.1), compressao_frac=max(0.0, base_compressao - 0.1), eficacia_paralelismo=max(0.3, eficacia_paralelismo - 0.2), eficiencia_stream=max(0.3, eficiencia_stream - 0.1)),
        "realista": Scenario("realista", overhead_frac=base_overhead, compressao_frac=base_compressao, eficacia_paralelismo=eficacia_paralelismo, eficiencia_stream=eficiencia_stream),
        "otimista": Scenario("otimista", overhead_frac=max(0.0, base_overhead - 0.05), compressao_frac=min(0.9, base_compressao + 0.1), eficacia_paralelismo=min(1.0, eficacia_paralelismo + 0.2), eficiencia_stream=min(1.0, eficiencia_stream + 0.1)),
    }


def calcular_estimativa(
    dados_bytes: int,
    banda_bps: int,
    overhead_frac: float,
    compressao_frac: float,
    paralelismo: int,
    eficacia_paralelismo: float,
    janela_diaria_s: int,
    disponibilidade_s: int,
    nome_cenario: str,
    eficiencia_stream: float,
    override_bps_efetivo: float | None = None,
) -> Dict[str, object]:
    dados_pos = calcular_volume_pos_compressao(dados_bytes, compressao_frac)
    if override_bps_efetivo is not None and override_bps_efetivo > 0:
        bps_efetivo = override_bps_efetivo
    else:
        bps_efetivo = calcular_throughput_efetivo_bps(
            banda_bps,
            overhead_frac,
            paralelismo,
            eficacia_paralelismo,
            eficiencia_stream,
        )
    duracao_s = calcular_duracao_segundos(dados_pos, bps_efetivo)
    cronograma = estimar_cronograma(duracao_s, janela_diaria_s, disponibilidade_s)
    return {
        "cenario": nome_cenario,
        "dados_pos_compressao_gb": round(dados_pos / 1e9, 2),
        "throughput_mbps": round(bps_efetivo / 1e6, 2),
        "duracao_segundos": duracao_s,
        "duracao_formatada": formatar_duracao(duracao_s),
        "cronograma": cronograma,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculadora de tempo de replicação/migração baseada em banda, compressão e janelas",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--dados", type=parse_size, required=True, help="Tamanho total dos dados (ex: 5TB, 500GiB)")
    parser.add_argument("--banda", type=parse_bitrate, required=True, help="Largura de banda (ex: 1Gbps, 500Mbps)")

    # Modo simples com perfis
    parser.add_argument("--simples", action="store_true", help="Modo simples: usa perfis para assumir overhead/compressão/eficiências")
    parser.add_argument("--perfil", choices=["fastconnect", "vpn", "internet", "lan"], default="fastconnect", help="Perfil de rede para o modo simples")

    # Parâmetros detalhados (avançado)
    parser.add_argument("--overhead", type=parse_percentage, default="15%", help="Overhead de rede/protocolo (ex: 15%)")
    parser.add_argument("--compressao", type=parse_percentage, default="0%", help="Redução por compressão (ex: 30% para reduzir 30% do volume)")
    parser.add_argument("--paralelismo", type=int, default=1, help="Número de fluxos paralelos (ex: 4)")
    parser.add_argument("--eficacia-paralelismo", dest="eficacia", type=float, default=0.7, help="Eficiência do paralelismo (0..1)")
    parser.add_argument("--eficiencia-stream", dest="ef_stream", type=float, default=DEFAULT_STREAM_EFFICIENCY, help="Eficiência de um único fluxo (0..1)")

    # Janelas e disponibilidade
    parser.add_argument("--janela", type=parse_time_window, default="8h", help="Janela diária de execução (ex: 8h)")
    parser.add_argument("--disponibilidade", type=parse_time_window, default="0d", help="Disponibilidade total (ex: 7d). 0d significa sem limite.")

    # Cenário e formato
    parser.add_argument("--cenario", choices=["pessimista", "realista", "otimista", "todos"], default="realista", help="Cenário a considerar")
    parser.add_argument("--saida", choices=["tabela", "csv", "md", "json"], default="tabela", help="Formato de saída")

    # Override direto do throughput efetivo
    parser.add_argument("--mbps-efetivo", type=float, default=None, help="Se informado, usa este throughput efetivo (em Mbps) e ignora overhead/paralelismo")

    args = parser.parse_args()

    # Seleção de parâmetros conforme modo simples ou avançado
    if args.simples:
        perf = perfil_defaults(args.perfil)
        overhead = float(perf["overhead"])  # type: ignore
        compressao = float(perf["compressao"])  # type: ignore
        eficacia = float(perf["eficacia"])  # type: ignore
        paralelismo = int(perf["paralelismo"])  # type: ignore
        ef_stream = float(perf["eficiencia_stream"])  # type: ignore
    else:
        overhead = args.overhead
        compressao = args.compressao
        eficacia = args.eficacia
        paralelismo = args.paralelismo
        ef_stream = args.ef_stream

    cenarios = montar_cenarios(overhead, compressao, eficacia, ef_stream)

    resultados: List[Dict[str, object]] = []

    override_bps = None
    if args.mbps_efetivo is not None and args.mbps_efetivo > 0:
        override_bps = args.mbps_efetivo * 1e6

    def produzir(cen: Scenario) -> Dict[str, object]:
        return calcular_estimativa(
            dados_bytes=args.dados,
            banda_bps=args.banda,
            overhead_frac=cen.overhead_frac,
            compressao_frac=cen.compressao_frac,
            paralelismo=paralelismo,
            eficacia_paralelismo=cen.eficacia_paralelismo,
            janela_diaria_s=args.janela,
            disponibilidade_s=args.disponibilidade,
            nome_cenario=cen.nome,
            eficiencia_stream=cen.eficiencia_stream,
            override_bps_efetivo=override_bps,
        )

    if args.cenario == "todos":
        for key in ("pessimista", "realista", "otimista"):
            resultados.append(produzir(cenarios[key]))
    else:
        resultados.append(produzir(cenarios[args.cenario]))

    # Emissão
    if args.saida == "json":
        print(json.dumps(resultados if len(resultados) > 1 else resultados[0], ensure_ascii=False, indent=2))
        return

    if args.saida == "csv":
        # Se vários cenários, imprime múltiplas linhas
        linhas = []
        for r in resultados:
            linhas.append(formatar_csv(r))
        # cabeçalho duplicado por linha; para uso simples, mantemos por cenário
        print("\n".join(linhas))
        return

    if args.saida == "md":
        blocos = []
        for r in resultados:
            blocos.append(f"\n### Cenário: {r['cenario']}\n\n" + formatar_markdown(r))
        print("\n".join(blocos))
        return

    # padrão: tabela
    for r in resultados:
        print(formatar_tabela_resultado(r))
        print()


if __name__ == "__main__":
    main()
