"""
Locus · Índice de Aderência Territorial (IAT)
=============================================
Implementação do método de scoring territorial da Locus
Inteligência de Mercado para avaliação de abertura de negócios
por bairro.

Autor: Andrade / Locus Inteligência de Mercado
São Gonçalo, RJ · 2026
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec
from math import pi
import warnings
warnings.filterwarnings("ignore")

# ── Configuração visual ──────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor":   "#161b22",
    "axes.edgecolor":   "#21262d",
    "axes.labelcolor":  "#c9d1d9",
    "xtick.color":      "#8b949e",
    "ytick.color":      "#8b949e",
    "text.color":       "#c9d1d9",
    "grid.color":       "#21262d",
    "grid.linestyle":   "--",
    "grid.alpha":       0.4,
    "font.family":      "DejaVu Sans",
})

COR_IDEAL      = "#06d6a0"  # 80-100
COR_FAVORAVEL  = "#00b4d8"  # 65-79
COR_NEUTRO     = "#f77f00"  # 50-64
COR_DESAFIADOR = "#e63946"  # 35-49
COR_INVIAVEL   = "#6e0d25"  # 0-34

def cor_por_iat(score):
    if score >= 80: return COR_IDEAL
    if score >= 65: return COR_FAVORAVEL
    if score >= 50: return COR_NEUTRO
    if score >= 35: return COR_DESAFIADOR
    return COR_INVIAVEL

def classificacao(score):
    if score >= 80: return "Território Ideal"
    if score >= 65: return "Território Favorável"
    if score >= 50: return "Território Neutro"
    if score >= 35: return "Território Desafiador"
    return "Território Inviável"

def veredito(score):
    if score >= 65: return "ABRIR"
    if score >= 50: return "APROFUNDAR"
    if score >= 35: return "ALTO RISCO"
    return "NÃO RECOMENDADO"


# ════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPAL — IATCalculator
# ════════════════════════════════════════════════════════════════════════════

class IATCalculator:
    """
    Calcula o Índice de Aderência Territorial (IAT) para uma combinação
    de bairro × categoria de negócio.

    O IAT é composto por 3 componentes com peso igual:
        C1 · Potencial do Território  (infraestrutura, renda, densidade)
        C2 · Aderência do Consumidor  (perfil etário, ticket, frequência)
        C3 · Janela Competitiva       (concorrência, qualidade, tendência)

    Cada componente é calculado como média ponderada de seus subfatores,
    todos normalizados em escala 0–100.
    """

    # Pesos dos componentes no IAT final
    PESOS_COMPONENTES = {"c1": 1/3, "c2": 1/3, "c3": 1/3}

    # Subfatores e pesos dentro de cada componente
    SUBFATORES = {
        "c1": {
            "densidade_populacional": 0.30,
            "renda_adequada_ticket":  0.30,
            "mobilidade_acesso":      0.25,
            "infraestrutura_basica":  0.15,
        },
        "c2": {
            "perfil_etario":          0.30,
            "demanda_digital":        0.20,
            "frequencia_consumo":     0.25,
            "compatibilidade_ticket": 0.25,
        },
        "c3": {
            "densidade_concorrencia": 0.30,
            "gap_qualidade":          0.30,
            "tendencia_setor":        0.25,
            "barreira_redes":         0.15,
        },
    }

    def __init__(self, territorio: str, categoria: str):
        self.territorio = territorio
        self.categoria  = categoria
        self.inputs     = {}
        self.scores     = {}
        self.ic         = 5  # Intervalo de Confiança padrão

    def carregar_inputs(self, inputs: dict):
        """
        Recebe um dicionário com os scores brutos (0–100) de cada subfator.
        Estrutura esperada:
        {
          "c1": {"densidade_populacional": 70, "renda_adequada_ticket": 75, ...},
          "c2": {...},
          "c3": {...},
          "ic": 5   # opcional — intervalo de confiança
        }
        """
        self.inputs = inputs
        if "ic" in inputs:
            self.ic = inputs["ic"]
        return self

    def _calcular_componente(self, componente: str) -> float:
        """Média ponderada dos subfatores de um componente."""
        pesos   = self.SUBFATORES[componente]
        valores = self.inputs[componente]
        score   = sum(pesos[sf] * valores[sf] for sf in pesos)
        return round(score, 2)

    def calcular(self) -> dict:
        """Calcula o IAT completo e retorna o resultado estruturado."""
        c1 = self._calcular_componente("c1")
        c2 = self._calcular_componente("c2")
        c3 = self._calcular_componente("c3")

        iat = round(
            c1 * self.PESOS_COMPONENTES["c1"] +
            c2 * self.PESOS_COMPONENTES["c2"] +
            c3 * self.PESOS_COMPONENTES["c3"],
            1
        )

        self.scores = {
            "territorio":      self.territorio,
            "categoria":       self.categoria,
            "c1":              c1,
            "c2":              c2,
            "c3":              c3,
            "iat":             iat,
            "ic":              self.ic,
            "iat_min":         max(0,   round(iat - self.ic, 1)),
            "iat_max":         min(100, round(iat + self.ic, 1)),
            "classificacao":   classificacao(iat),
            "veredito":        veredito(iat),
        }
        return self.scores

    def relatorio_texto(self) -> str:
        s = self.scores
        linha = "─" * 58
        return f"""
{linha}
LOCUS · IAT — {s['territorio'].upper()}
Categoria: {s['categoria']}
{linha}
  C1 · Potencial do Território  : {s['c1']:>6.1f}
  C2 · Aderência do Consumidor  : {s['c2']:>6.1f}
  C3 · Janela Competitiva       : {s['c3']:>6.1f}
{linha}
  IAT FINAL  : {s['iat']:>5.1f}  ±{s['ic']}
  Intervalo  : [{s['iat_min']} – {s['iat_max']}]
  Classe     : {s['classificacao']}
  Veredito   : {s['veredito']}
{linha}
"""


# ════════════════════════════════════════════════════════════════════════════
# DADOS DO RELATÓRIO PILOTO — BAIRRO CAMARÃO
# ════════════════════════════════════════════════════════════════════════════

CAMARAO_DATA = {
    "Alimentação": {
        "ic": 5,
        "c1": {
            "densidade_populacional": 68,
            "renda_adequada_ticket":  75,
            "mobilidade_acesso":      80,
            "infraestrutura_basica":  70,
        },
        "c2": {
            "perfil_etario":          80,
            "demanda_digital":        70,
            "frequencia_consumo":     75,
            "compatibilidade_ticket": 72,
        },
        "c3": {
            "densidade_concorrencia": 60,
            "gap_qualidade":          70,
            "tendencia_setor":        65,
            "barreira_redes":         65,
        },
    },
    "Saúde & Bem-Estar": {
        "ic": 7,
        "c1": {
            "densidade_populacional": 68,
            "renda_adequada_ticket":  62,
            "mobilidade_acesso":      80,
            "infraestrutura_basica":  70,
        },
        "c2": {
            "perfil_etario":          65,
            "demanda_digital":        55,
            "frequencia_consumo":     58,
            "compatibilidade_ticket": 60,
        },
        "c3": {
            "densidade_concorrencia": 38,
            "gap_qualidade":          50,
            "tendencia_setor":        45,
            "barreira_redes":         40,
        },
    },
    "Serviços (Barbearia)": {
        "ic": 4,
        "c1": {
            "densidade_populacional": 68,
            "renda_adequada_ticket":  72,
            "mobilidade_acesso":      80,
            "infraestrutura_basica":  70,
        },
        "c2": {
            "perfil_etario":          88,
            "demanda_digital":        78,
            "frequencia_consumo":     85,
            "compatibilidade_ticket": 80,
        },
        "c3": {
            "densidade_concorrencia": 82,
            "gap_qualidade":          80,
            "tendencia_setor":        78,
            "barreira_redes":         75,
        },
    },
}

# Salva os inputs em JSON para rastreabilidade
import os
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

with open("data/camarao_inputs.json", "w", encoding="utf-8") as f:
    json.dump(CAMARAO_DATA, f, ensure_ascii=False, indent=2)


# ════════════════════════════════════════════════════════════════════════════
# EXECUÇÃO — Calcular IAT para todas as categorias
# ════════════════════════════════════════════════════════════════════════════

resultados = []
calculadoras = {}

for categoria, dados in CAMARAO_DATA.items():
    calc = IATCalculator(territorio="Camarão · São Gonçalo", categoria=categoria)
    calc.carregar_inputs(dados)
    resultado = calc.calcular()
    resultados.append(resultado)
    calculadoras[categoria] = calc
    print(calc.relatorio_texto())

df = pd.DataFrame(resultados)
df.to_csv("outputs/relatorio_camarao.csv", index=False)
print("✓ CSV exportado: outputs/relatorio_camarao.csv\n")


# ════════════════════════════════════════════════════════════════════════════
# VISUALIZAÇÃO 1 — Painel comparativo IAT
# ════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(16, 9))
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

ax_main = fig.add_subplot(gs[0, :])   # barra horizontal principal
ax_c1   = fig.add_subplot(gs[1, 0])
ax_c2   = fig.add_subplot(gs[1, 1])
ax_c3   = fig.add_subplot(gs[1, 2])

fig.patch.set_facecolor("#0d1117")

# ── Painel principal: IAT com IC ──────────────────────────────────────────
categorias = df["categoria"].tolist()
iats       = df["iat"].tolist()
ics        = df["ic"].tolist()
cores      = [cor_por_iat(v) for v in iats]
vereditos  = df["veredito"].tolist()

y = range(len(categorias))
bars = ax_main.barh(y, iats, color=cores, alpha=0.85, height=0.5)
ax_main.errorbar(iats, list(y), xerr=ics, fmt="none",
                 ecolor="#ffffff", elinewidth=1.5, capsize=6, capthick=1.5)

# Escala de classificação (fundo)
for limite, cor, label in [
    (35, "#6e0d25", "Inviável"), (50, "#e63946", "Desafiador"),
    (65, "#f77f00", "Neutro"),   (80, "#00b4d8", "Favorável"), (100, "#06d6a0", "Ideal")
]:
    ax_main.axvline(limite, color=cor, linestyle=":", linewidth=0.8, alpha=0.5)

for bar, iat, ic, verd, cor in zip(bars, iats, ics, vereditos, cores):
    ax_main.text(iat + ic + 1, bar.get_y() + bar.get_height()/2,
                 f"  {iat:.0f} ±{ic}  [{verd}]",
                 va="center", fontsize=11, fontweight="bold", color=cor)

ax_main.set_yticks(list(y))
ax_main.set_yticklabels(categorias, fontsize=12)
ax_main.set_xlim(0, 115)
ax_main.set_xlabel("IAT (0–100)")
ax_main.set_title("IAT por Categoria · Bairro Camarão · São Gonçalo (março/2026)",
                   fontsize=14, fontweight="bold", pad=12, color="#ffffff")
ax_main.set_facecolor("#161b22")

# ── Sub-painéis: C1, C2, C3 ──────────────────────────────────────────────
comp_labels = {"c1": "C1 · Potencial do Território",
               "c2": "C2 · Aderência do Consumidor",
               "c3": "C3 · Janela Competitiva"}

for ax, comp, ax_label in zip([ax_c1, ax_c2, ax_c3],
                               ["c1", "c2", "c3"],
                               comp_labels.values()):
    vals = df[comp].tolist()
    ax.barh(categorias, vals, color=[cor_por_iat(v) for v in vals], alpha=0.8, height=0.5)
    for i, v in enumerate(vals):
        ax.text(v + 1, i, f"{v:.0f}", va="center", fontsize=9, color="#c9d1d9")
    ax.set_xlim(0, 100)
    ax.set_title(ax_label, fontsize=9, color="#8b949e", pad=6)
    ax.set_facecolor("#161b22")
    ax.tick_params(labelsize=8)

plt.savefig("outputs/01_iat_comparativo.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
plt.close()
print("✓ Gráfico 1: IAT comparativo")


# ════════════════════════════════════════════════════════════════════════════
# VISUALIZAÇÃO 2 — Radar por categoria
# ════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(16, 6),
                          subplot_kw=dict(polar=True))
fig.patch.set_facecolor("#0d1117")
fig.suptitle("Perfil por Componente (Radar) · Camarão", fontsize=14,
             fontweight="bold", color="#ffffff", y=1.02)

labels_radar = ["C1\nTerritório", "C2\nConsumidor", "C3\nCompetitivo"]
N = 3
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

for ax, row, cor in zip(axes, resultados, [COR_FAVORAVEL, COR_NEUTRO, COR_IDEAL]):
    vals = [row["c1"], row["c2"], row["c3"]]
    vals += vals[:1]

    ax.set_facecolor("#161b22")
    ax.plot(angles, vals, "o-", linewidth=2, color=cor)
    ax.fill(angles, vals, alpha=0.25, color=cor)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels_radar, size=10, color="#c9d1d9")
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25", "50", "75", "100"], size=7, color="#8b949e")
    ax.grid(color="#21262d", linewidth=0.8)
    ax.spines["polar"].set_color("#21262d")

    iat = row["iat"]
    ax.set_title(f"{row['categoria']}\nIAT {iat:.0f} · {row['classificacao']}",
                 pad=18, fontsize=10, fontweight="bold", color=cor)

plt.tight_layout()
plt.savefig("outputs/02_radar_componentes.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
plt.close()
print("✓ Gráfico 2: radar por componente")


# ════════════════════════════════════════════════════════════════════════════
# VISUALIZAÇÃO 3 — Análise de sensibilidade de pesos
# ════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.patch.set_facecolor("#0d1117")
fig.suptitle("Sensibilidade do IAT à Variação de Pesos · Camarão",
             fontsize=14, fontweight="bold", color="#ffffff")

peso_range = np.linspace(0.1, 0.6, 50)

for ax, row, cor in zip(axes, resultados, [COR_FAVORAVEL, COR_NEUTRO, COR_IDEAL]):
    iats_c1, iats_c2, iats_c3 = [], [], []
    for p in peso_range:
        resto = (1 - p) / 2
        iats_c1.append(row["c1"] * p + row["c2"] * resto + row["c3"] * resto)
        iats_c2.append(row["c1"] * resto + row["c2"] * p + row["c3"] * resto)
        iats_c3.append(row["c1"] * resto + row["c2"] * resto + row["c3"] * p)

    ax.plot(peso_range, iats_c1, label="Peso ↑ C1", color=COR_FAVORAVEL, linewidth=2)
    ax.plot(peso_range, iats_c2, label="Peso ↑ C2", color=COR_NEUTRO,   linewidth=2)
    ax.plot(peso_range, iats_c3, label="Peso ↑ C3", color=COR_IDEAL,    linewidth=2)

    ax.axhline(65, color="#ffffff", linestyle="--", linewidth=0.8, alpha=0.5, label="Limite Favorável")
    ax.axhline(50, color="#f77f00", linestyle="--", linewidth=0.8, alpha=0.5, label="Limite Neutro")
    ax.axvline(1/3, color="#8b949e", linestyle=":", linewidth=1, alpha=0.7, label="Peso atual (1/3)")

    ax.set_facecolor("#161b22")
    ax.set_title(f"{row['categoria']}", fontsize=10, color=cor, fontweight="bold")
    ax.set_xlabel("Peso do componente selecionado")
    ax.set_ylabel("IAT resultante")
    ax.set_ylim(30, 100)
    ax.legend(fontsize=7, framealpha=0.2)

plt.tight_layout()
plt.savefig("outputs/03_sensibilidade.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
plt.close()
print("✓ Gráfico 3: análise de sensibilidade")


# ════════════════════════════════════════════════════════════════════════════
# RESUMO FINAL
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 58)
print("LOCUS · RESUMO FINAL — BAIRRO CAMARÃO")
print("═" * 58)
for r in resultados:
    iat = r["iat"]
    cor_txt = {"ABRIR": "✅", "APROFUNDAR": "⚠️ ", "ALTO RISCO": "🔴"}.get(r["veredito"], "❓")
    print(f"{cor_txt}  {r['categoria']:<25} IAT {iat:>5.1f} ±{r['ic']}  →  {r['veredito']}")

print("═" * 58)
print("\n✅ Pipeline completo. Outputs em /outputs/")
print("   Locus · inteligência do lugar · São Gonçalo, RJ · 2026")
