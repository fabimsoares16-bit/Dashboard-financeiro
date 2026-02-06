"""
Módulo de visualizações com Plotly.

Funções para gerar gráficos do dashboard financeiro.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Paleta de cores para categorias
CORES_CATEGORIAS = [
    "#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4",
    "#ffeaa7", "#dfe6e9", "#fd79a8", "#6c5ce7",
    "#00b894", "#e17055", "#0984e3", "#fdcb6e",
]

CORES_TIPO = ["#ff6b6b", "#4ecdc4"]


def grafico_pizza_tipo(fixos: float, variaveis: float) -> go.Figure:
    """Gráfico de pizza: Fixos vs Variáveis."""
    df = pd.DataFrame({
        "Tipo": ["Fixos", "Variáveis"],
        "Valor": [fixos, variaveis]
    })
    fig = px.pie(
        df, names="Tipo", values="Valor",
        title="Fixos vs Variáveis",
        color_discrete_sequence=CORES_TIPO,
        hole=0.4,
    )
    fig.update_traces(textinfo="percent+label+value", texttemplate="%{label}<br>R$ %{value:.2f}<br>(%{percent})")
    fig.update_layout(title_x=0.5, showlegend=False)
    return fig


def grafico_pizza_categorias(gastos: list[dict]) -> go.Figure:
    """Gráfico de pizza com distribuição por categoria."""
    df = pd.DataFrame(gastos)
    if df.empty:
        return None
    agrupado = df.groupby("categoria")["valor"].sum().reset_index()
    agrupado.columns = ["Categoria", "Valor"]
    agrupado = agrupado.sort_values("Valor", ascending=False)

    fig = px.pie(
        agrupado, names="Categoria", values="Valor",
        title="Gastos por Categoria",
        color_discrete_sequence=CORES_CATEGORIAS,
        hole=0.4,
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title_x=0.5)
    return fig


def grafico_evolucao_mensal(meses: list[str], totais: list[float], salario: float) -> go.Figure:
    """Gráfico de linha com evolução mensal dos gastos e linha do salário."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=meses, y=totais,
        mode="lines+markers",
        name="Gastos",
        line=dict(color="#ff6b6b", width=3),
        marker=dict(size=8),
    ))

    if salario > 0:
        fig.add_trace(go.Scatter(
            x=meses, y=[salario] * len(meses),
            mode="lines",
            name="Salário",
            line=dict(color="#4ecdc4", width=2, dash="dash"),
        ))

    fig.update_layout(
        title="Evolução Mensal",
        title_x=0.5,
        xaxis_title="Mês",
        yaxis_title="Valor (R$)",
        hovermode="x unified",
    )
    return fig


def grafico_barras_categorias(gastos: list[dict]) -> go.Figure:
    """Gráfico de barras horizontais com valores por categoria."""
    df = pd.DataFrame(gastos)
    if df.empty:
        return None
    agrupado = df.groupby("categoria")["valor"].sum().reset_index()
    agrupado.columns = ["Categoria", "Valor"]
    agrupado = agrupado.sort_values("Valor", ascending=True)

    fig = px.bar(
        agrupado, x="Valor", y="Categoria",
        orientation="h",
        title="Gastos por Categoria",
        color="Valor",
        color_continuous_scale=["#4ecdc4", "#ff6b6b"],
    )
    fig.update_layout(
        title_x=0.5,
        showlegend=False,
        coloraxis_showscale=False,
    )
    fig.update_traces(texttemplate="R$ %{x:.2f}", textposition="outside")
    return fig


def grafico_meta_vs_gasto(gasto_total: float, meta: float, mes: str) -> go.Figure:
    """Gráfico de gauge mostrando progresso em relação à meta."""
    percentual = (gasto_total / meta * 100) if meta > 0 else 0

    if percentual <= 80:
        bar_color = "#00b894"
    elif percentual <= 100:
        bar_color = "#fdcb6e"
    else:
        bar_color = "#ff6b6b"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=gasto_total,
        number={"prefix": "R$ ", "valueformat": ",.2f"},
        delta={"reference": meta, "valueformat": ",.2f", "prefix": "R$ "},
        title={"text": f"Meta de {mes}"},
        gauge={
            "axis": {"range": [0, max(meta * 1.2, gasto_total * 1.1)]},
            "bar": {"color": bar_color},
            "steps": [
                {"range": [0, meta * 0.8], "color": "#e8f5e9"},
                {"range": [meta * 0.8, meta], "color": "#fff3e0"},
                {"range": [meta, max(meta * 1.2, gasto_total * 1.1)], "color": "#ffebee"},
            ],
            "threshold": {
                "line": {"color": "#2d3436", "width": 3},
                "thickness": 0.8,
                "value": meta,
            },
        },
    ))
    fig.update_layout(height=300)
    return fig
