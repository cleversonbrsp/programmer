# -*- coding: utf-8 -*-

import json
import math
import streamlit as st

from replication_calc import (
    parse_size,
    parse_bitrate,
    parse_time_window,
    perfil_defaults,
    montar_cenarios,
    calcular_estimativa,
    formatar_markdown,
    formatar_csv,
)

st.set_page_config(page_title="Estimativa de Replicação", page_icon="⚡", layout="wide")

# ==========================
# Estilo Futurista (Glass)
# ==========================
GLASS_CSS = """
<style>
/* Background gradiente futurista */
.stApp {
  background: radial-gradient(1200px 600px at 5% 0%, #0f1120 0, #0b0d19 45%, #080a14 100%);
  color: #e6e8ff;
}

/* Cards glassmorphism */
.glass {
  background: rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: 18px 22px;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.metric .label {
  color: #aab0ff;
  font-size: 12px;
  letter-spacing: .4px;
  text-transform: uppercase;
}
.metric .value {
  font-size: 28px;
  font-weight: 700;
  color: #ffffff;
}
.metric .subvalue {
  font-size: 12px;
  color: #9aa3b2;
}

hr {
  border: none;
  height: 1px;
  background: linear-gradient(to right, rgba(255,255,255,.15), rgba(255,255,255,.04));
}

/* Botões */
.stButton>button {
  background: linear-gradient(135deg, #6b73ff 0%, #000dff 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 8px 14px;
}
.stButton>button:hover { filter: brightness(1.05); }

/* Inputs */
.stNumberInput, .stTextInput, .stSelectbox, .stSlider {
  color: #e6e8ff !important;
}

.block-title {
  font-size: 14px;
  color: #aab0ff;
  text-transform: uppercase;
  letter-spacing: .5px;
}

.title {
  font-weight: 800;
  font-size: 34px;
}
.subtitle { color: #aab0ff; }
</style>
"""

st.markdown(GLASS_CSS, unsafe_allow_html=True)

# ==========================
# Cabeçalho
# ==========================
col_title, col_logo = st.columns([0.8, 0.2])
with col_title:
    st.markdown('<div class="title">⚡ Estimativa de Replicação Rackware</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Moderno, simples e comparativo por cenários</div>', unsafe_allow_html=True)
with col_logo:
    st.markdown("""
    <div style="text-align:right;opacity:.9" class="glass">
      <div class="metric"><span class="label">versão</span>
      <span class="value">1.0</span>
      <span class="subvalue">by Cleverson Rodrigues</span></div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================
# Sidebar (Modo)
# ==========================
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    modo_simples = st.toggle("Modo simples (recomendado)", value=True, help="Usa perfis para assumir overhead, compressão e eficiências")
    cen_choice = st.selectbox("Cenário", ["realista", "pessimista", "otimista", "todos"], index=0)
    show_details = st.checkbox("Mostrar detalhes do cálculo", value=False)

# ==========================
# Entradas
# ==========================
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="block-title">Dados e Rede</div>', unsafe_allow_html=True)
    with st.container():
        with st.expander("Dados", expanded=True):
            n_dados = st.number_input("Tamanho dos dados", min_value=0.0, value=5.0, step=0.5)
            u_dados = st.selectbox("Unidade", ["GB", "TB", "TiB"], index=1)
        with st.expander("Rede", expanded=True):
            n_banda = st.number_input("Banda contratada", min_value=0.0, value=1.0, step=0.1)
            u_banda = st.selectbox("Unidade", ["Mbps", "Gbps"], index=1)
            janela_h = st.number_input("Janela diária (horas)", min_value=1, value=8, step=1)
            disponibilidade_d = st.number_input("Disponibilidade total (dias)", min_value=0, value=7, step=1)

with col_right:
    st.markdown('<div class="block-title">Ajustes</div>', unsafe_allow_html=True)
    with st.container():
        if modo_simples:
            perfil = st.selectbox("Perfil de rede", ["fastconnect", "vpn", "internet", "lan"], index=0)
            mbps_efetivo = st.number_input("Override de taxa efetiva (Mbps) — opcional", min_value=0.0, value=0.0, step=50.0, help="Se preenchido, ignora detalhes e usa esta taxa")
        else:
            overhead = st.slider("Overhead de rede (%)", min_value=0, max_value=50, value=15, step=1)
            compressao = st.slider("Compressão / Redução (%)", min_value=0, max_value=90, value=30, step=5)
            paralelismo = st.number_input("Paralelismo (streams)", min_value=1, value=4, step=1)
            eficacia = st.slider("Eficiência do paralelismo", min_value=0.3, max_value=1.0, value=0.85, step=0.05)
            ef_stream = st.slider("Eficiência por stream", min_value=0.3, max_value=1.0, value=0.6, step=0.05)

st.write("")

# ==========================
# Botão Calcular
# ==========================
col_btn1, col_btn2 = st.columns([0.2, 0.8])
with col_btn1:
    clicked = st.button("Calcular", type="primary")

# ==========================
# Helpers
# ==========================

def build_value_with_unit(value: float, unit: str) -> str:
    # Garantir strings no formato aceito pelo parser do módulo
    v = ("%f" % value).rstrip("0").rstrip(".")
    return f"{v}{unit}"


def to_seconds(hours: int) -> int:
    return int(hours * 3600)


def to_seconds_days(days: int) -> int:
    return int(days * 86400)


def render_metric(label: str, value: str, subvalue: str = ""):
    st.markdown(
        f"""
        <div class="glass metric">
            <span class="label">{label}</span>
            <span class="value">{value}</span>
            <span class="subvalue">{subvalue}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================
# Cálculo
# ==========================
if clicked:
    try:
        dados_str = build_value_with_unit(n_dados, u_dados)
        banda_str = build_value_with_unit(n_banda, u_banda)

        dados_bytes = parse_size(dados_str)
        banda_bps = parse_bitrate(banda_str)
        janela_s = to_seconds(janela_h)
        disp_s = to_seconds_days(disponibilidade_d)

        if modo_simples:
            perf = perfil_defaults(perfil)
            overhead = float(perf["overhead"])  # type: ignore
            compressao = float(perf["compressao"])  # type: ignore
            eficacia = float(perf["eficacia"])  # type: ignore
            paralelismo = int(perf["paralelismo"])  # type: ignore
            ef_stream = float(perf["eficiencia_stream"])  # type: ignore
        else:
            # já coletados acima nos controles avançados
            pass

        cenarios = montar_cenarios(overhead, compressao, eficacia, ef_stream)

        override_bps = None
        if modo_simples and mbps_efetivo and mbps_efetivo > 0:
            override_bps = mbps_efetivo * 1e6

        def produzir(nome: str):
            cen = cenarios[nome]
            return calcular_estimativa(
                dados_bytes=dados_bytes,
                banda_bps=banda_bps,
                overhead_frac=cen.overhead_frac,
                compressao_frac=cen.compressao_frac,
                paralelismo=paralelismo,
                eficacia_paralelismo=cen.eficacia_paralelismo,
                janela_diaria_s=janela_s,
                disponibilidade_s=disp_s,
                nome_cenario=cen.nome,
                eficiencia_stream=cen.eficiencia_stream,
                override_bps_efetivo=override_bps,
            )

        resultados = []
        nomes = [cen_choice] if cen_choice != "todos" else ["pessimista", "realista", "otimista"]
        for n in nomes:
            resultados.append(produzir(n))

        # ==========================
        # Exibição
        # ==========================
        st.markdown("<hr>", unsafe_allow_html=True)
        cols = st.columns(len(resultados))
        for c, r in zip(cols, resultados):
            with c:
                render_metric("Cenário", r["cenario"].capitalize())
                render_metric("Dados pós-comp.", f"{r['dados_pos_compressao_gb']} GB")
                render_metric("Throughput efetivo", f"{r['throughput_mbps']} Mbps")
                render_metric("Duração", r["duracao_formatada"]) 
                cj = r["cronograma"]
                render_metric("Janelas necessárias", str(cj["janelas_necessarias"]))
                render_metric("Dias totais", str(cj["dias_totais"]))
                render_metric("Dentro do prazo", "Sim" if cj["dentro_disponibilidade"] else "Não")

        # Detalhes
        if show_details:
            st.markdown("## Detalhes")
            for r in resultados:
                st.markdown(f"### {r['cenario'].capitalize()}")
                st.json(r)

        # Downloads
        st.markdown("## Downloads")
        if len(resultados) == 1:
            r = resultados[0]
            st.download_button("CSV", data=formatar_csv(r), file_name=f"estimativa_{r['cenario']}.csv")
            st.download_button("Markdown", data=formatar_markdown(r), file_name=f"estimativa_{r['cenario']}.md")
            st.download_button("JSON", data=json.dumps(r, ensure_ascii=False, indent=2), file_name=f"estimativa_{r['cenario']}.json")
        else:
            # múltiplos cenários -> gerar pacotinho simples
            csv_data = "\n\n".join(formatar_csv(r) for r in resultados)
            md_data = "\n\n".join((f"### {r['cenario'].capitalize()}\n\n" + formatar_markdown(r)) for r in resultados)
            json_data = json.dumps(resultados, ensure_ascii=False, indent=2)
            st.download_button("CSV (cenários)", data=csv_data, file_name="estimativas_cenarios.csv")
            st.download_button("Markdown (cenários)", data=md_data, file_name="estimativas_cenarios.md")
            st.download_button("JSON (cenários)", data=json_data, file_name="estimativas_cenarios.json")

    except Exception as e:
        st.error(f"Erro: {e}")
        st.stop()
