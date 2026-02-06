"""
Dashboard Financeiro Interativo Para Gestão Pessoal de Despesas.

Criar o ambiente virtual: python3 -m venv .venv

Ativar o ambiente virtual em Windows: .venv\\Scripts\\Activate

Ativar o ambiente virtual em MAC/LINUX: source .venv/bin/activate

Instalar as bibliotecas necessárias: pip install -r requirements.txt

Rodar a aplicação: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from src.database import (
    adicionar_gasto,
    remover_gasto,
    editar_gasto,
    obter_gastos_mes,
    obter_todos_gastos,
    limpar_tudo,
    importar_gastos,
    salvar_configuracao,
    obter_configuracao,
    salvar_meta,
    obter_meta,
    obter_todas_metas,
)
from src.charts import (
    grafico_pizza_tipo,
    grafico_pizza_categorias,
    grafico_evolucao_mensal,
    grafico_barras_categorias,
    grafico_meta_vs_gasto,
)

# Configurações iniciais da página Streamlit
st.set_page_config(layout="wide", page_title="Dashboard Financeiro", page_icon="💰")

# -------------------------
# Constantes
# -------------------------
MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]

CATEGORIAS = [
    "Moradia", "Alimentação", "Transporte", "Saúde", "Educação",
    "Lazer", "Vestuário", "Serviços", "Investimentos", "Outros",
]

# -------------------------
# Inicialização dos estados
# -------------------------
if "mes_selecionado" not in st.session_state:
    st.session_state.mes_selecionado = "Janeiro"

if "editando_id" not in st.session_state:
    st.session_state.editando_id = None

if "confirmar_limpar" not in st.session_state:
    st.session_state.confirmar_limpar = False

# Carregar salário do banco de dados
salario_salvo = float(obter_configuracao("salario", "0"))

# -------------------------
# Funções auxiliares
# -------------------------

def somar_por_tipo(mes: str) -> tuple[float, float, float]:
    """Soma os valores dos gastos do mês por tipo (Fixo/Variável)."""
    gastos = obter_gastos_mes(mes)
    fixos = sum(g["valor"] for g in gastos if g["tipo"] == "Fixo")
    variaveis = sum(g["valor"] for g in gastos if g["tipo"] == "Variável")
    return fixos, variaveis, fixos + variaveis


def totais_mensais() -> dict[str, float]:
    """Calcula o total de gastos para cada mês."""
    todos = obter_todos_gastos()
    totais = {m: 0.0 for m in MESES}
    for g in todos:
        if g["mes"] in totais:
            totais[g["mes"]] += g["valor"]
    return totais


def exportar_csv() -> bytes:
    """Gera um CSV com todos os gastos e o salário atual."""
    gastos = obter_todos_gastos()
    if not gastos:
        return b""
    df = pd.DataFrame(gastos)
    df = df[["mes", "tipo", "categoria", "descricao", "valor"]]
    df["salario"] = salario
    return df.to_csv(index=False).encode("utf-8")


def importar_csv(arquivo) -> None:
    """Importa um CSV e popula o banco de dados."""
    try:
        df = pd.read_csv(arquivo)
        colunas_obrigatorias = {"mes", "tipo", "descricao", "valor"}
        if not colunas_obrigatorias.issubset(set(df.columns)):
            st.error(f"CSV deve conter as colunas: {', '.join(colunas_obrigatorias)}")
            return

        gastos = []
        for _, row in df.iterrows():
            gastos.append({
                "mes": str(row["mes"]),
                "tipo": str(row["tipo"]),
                "categoria": str(row.get("categoria", "Outros")),
                "descricao": str(row["descricao"]),
                "valor": float(row["valor"]),
            })
        importar_gastos(gastos)

        if "salario" in df.columns:
            sal = float(df["salario"].iloc[0])
            salvar_configuracao("salario", str(sal))

        st.success(f"Dados importados: {len(gastos)} gastos carregados!")
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao importar CSV: {e}")


# -------------------------
# Layout principal
# -------------------------
st.title("💰 Dashboard Financeiro")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Configurações")

    novo_salario = st.number_input(
        "Salário mensal (R$)",
        min_value=0.0,
        value=salario_salvo,
        step=100.0,
        format="%.2f",
    )
    if novo_salario != salario_salvo:
        salvar_configuracao("salario", str(novo_salario))
    salario = novo_salario

    st.markdown("---")

    # --- Metas de economia ---
    st.subheader("🎯 Meta Mensal")
    mes_sel = st.session_state.mes_selecionado
    meta_atual = obter_meta(mes_sel)

    nova_meta = st.number_input(
        f"Meta de gastos - {mes_sel} (R$)",
        min_value=0.0,
        value=meta_atual if meta_atual else 0.0,
        step=100.0,
        format="%.2f",
        help="Defina um limite de gastos para o mês selecionado",
    )
    if nova_meta > 0 and nova_meta != meta_atual:
        salvar_meta(mes_sel, nova_meta)
        st.success(f"Meta de {mes_sel} atualizada!")

    st.markdown("---")

    # --- Backup ---
    st.subheader("💾 Backup")
    todos_gastos = obter_todos_gastos()

    if todos_gastos:
        st.download_button(
            "⬇️ Exportar CSV",
            exportar_csv(),
            "backup_financeiro.csv",
            "text/csv",
            use_container_width=True,
        )

    arquivo_enviado = st.file_uploader("⬆️ Restaurar backup", type=["csv"])
    if arquivo_enviado and st.button("Carregar", use_container_width=True):
        importar_csv(arquivo_enviado)

    st.markdown("---")

    # --- Limpar tudo com confirmação ---
    if not st.session_state.confirmar_limpar:
        if st.button("🗑️ Limpar tudo", use_container_width=True):
            st.session_state.confirmar_limpar = True
            st.rerun()
    else:
        st.warning("Tem certeza? Todos os dados serão apagados.")
        col_sim, col_nao = st.columns(2)
        with col_sim:
            if st.button("Sim", type="primary", use_container_width=True):
                limpar_tudo()
                st.session_state.confirmar_limpar = False
                st.rerun()
        with col_nao:
            if st.button("Não", use_container_width=True):
                st.session_state.confirmar_limpar = False
                st.rerun()

# ---------- Seleção de mês ----------
st.subheader("📅 Selecione o Mês")
colunas = st.columns(4)

for i, mes in enumerate(MESES):
    with colunas[i % 4]:
        _, _, total = somar_por_tipo(mes)
        meta = obter_meta(mes)
        esta_selecionado = st.session_state.mes_selecionado == mes

        if st.button(
            f"{'✓ ' if esta_selecionado else ''}{mes}",
            key=f"btn_{mes}",
            type="primary" if esta_selecionado else "secondary",
            use_container_width=True,
        ):
            st.session_state.mes_selecionado = mes
            st.session_state.editando_id = None
            st.rerun()

        # Mostra total e indicador de meta
        if total > 0:
            label = f"R$ {total:.2f}"
            if meta and total > meta:
                label += " ⚠️"
            st.caption(label)
        else:
            st.caption("Sem gastos")

st.markdown("---")

# ---------- Área principal ----------
selecionado = st.session_state.mes_selecionado
st.subheader(f"📊 {selecionado}")
col1, col2 = st.columns([2, 1])

with col1:
    # --- Formulário de adição ---
    st.markdown("### ➕ Adicionar Gasto")
    with st.form(key="formulario_adicionar", clear_on_submit=True):
        form_col1, form_col2 = st.columns(2)
        with form_col1:
            tipo = st.selectbox("Tipo", ["Fixo", "Variável"])
            descricao = st.text_input("Descrição", placeholder="Ex: Aluguel, Conta de luz...")
        with form_col2:
            categoria = st.selectbox("Categoria", CATEGORIAS)
            valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", step=10.0)

        if st.form_submit_button("✅ Adicionar", use_container_width=True):
            if not descricao.strip():
                st.error("Preencha a descrição.")
            elif valor <= 0:
                st.error("Valor deve ser maior que zero.")
            else:
                adicionar_gasto(selecionado, tipo, categoria, descricao.strip(), valor)
                st.success(f"Adicionado: {descricao} — R$ {valor:.2f} ({categoria})")
                st.rerun()

    # --- Tabela de gastos ---
    st.markdown("### 📋 Gastos Cadastrados")
    gastos_mes = obter_gastos_mes(selecionado)

    if not gastos_mes:
        st.info("Nenhum gasto cadastrado neste mês.")
    else:
        # Filtro por categoria
        categorias_presentes = sorted(set(g["categoria"] for g in gastos_mes))
        filtro_categorias = st.multiselect(
            "Filtrar por categoria",
            categorias_presentes,
            default=categorias_presentes,
            label_visibility="collapsed",
            placeholder="Filtrar por categoria...",
        )

        gastos_filtrados = [g for g in gastos_mes if g["categoria"] in filtro_categorias]

        if gastos_filtrados:
            df = pd.DataFrame(gastos_filtrados)
            df_display = df[["tipo", "categoria", "descricao", "valor"]].copy()
            df_display.columns = ["Tipo", "Categoria", "Descrição", "Valor"]
            df_display["Valor"] = df_display["Valor"].apply(lambda x: f"R$ {x:.2f}")
            st.dataframe(df_display, use_container_width=True, hide_index=True)

            # --- Edição de gasto ---
            if st.session_state.editando_id is not None:
                gasto_editando = next(
                    (g for g in gastos_mes if g["id"] == st.session_state.editando_id), None
                )
                if gasto_editando:
                    st.markdown("#### ✏️ Editando Gasto")
                    with st.form(key="formulario_editar"):
                        ed_col1, ed_col2 = st.columns(2)
                        with ed_col1:
                            ed_tipo = st.selectbox(
                                "Tipo", ["Fixo", "Variável"],
                                index=["Fixo", "Variável"].index(gasto_editando["tipo"]),
                            )
                            ed_descricao = st.text_input("Descrição", value=gasto_editando["descricao"])
                        with ed_col2:
                            ed_categoria = st.selectbox(
                                "Categoria", CATEGORIAS,
                                index=CATEGORIAS.index(gasto_editando["categoria"])
                                if gasto_editando["categoria"] in CATEGORIAS else len(CATEGORIAS) - 1,
                            )
                            ed_valor = st.number_input(
                                "Valor (R$)", min_value=0.01, value=gasto_editando["valor"], format="%.2f",
                            )

                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.form_submit_button("💾 Salvar", use_container_width=True):
                                editar_gasto(
                                    st.session_state.editando_id,
                                    ed_tipo, ed_categoria, ed_descricao.strip(), ed_valor,
                                )
                                st.session_state.editando_id = None
                                st.success("Gasto atualizado!")
                                st.rerun()
                        with btn_col2:
                            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                st.session_state.editando_id = None
                                st.rerun()

            # --- Ações: editar e remover ---
            opcoes = [
                f'{g["id"]}. {g["descricao"]} - R$ {g["valor"]:.2f} ({g["categoria"]})'
                for g in gastos_filtrados
            ]
            selecionado_gasto = st.selectbox(
                "Selecione um gasto", ["Selecione..."] + opcoes, label_visibility="collapsed",
            )

            if selecionado_gasto != "Selecione...":
                gasto_id = int(selecionado_gasto.split(".")[0])
                btn_edit, btn_del = st.columns(2)
                with btn_edit:
                    if st.button("✏️ Editar", use_container_width=True):
                        st.session_state.editando_id = gasto_id
                        st.rerun()
                with btn_del:
                    if st.button("🗑️ Remover", use_container_width=True, type="primary"):
                        remover_gasto(gasto_id)
                        st.success("Gasto removido!")
                        st.rerun()
        else:
            st.info("Nenhum gasto encontrado para os filtros selecionados.")

with col2:
    st.markdown("### 💵 Resumo")
    fixos, variaveis, total = somar_por_tipo(selecionado)
    saldo = salario - total

    st.metric("Salário", f"R$ {salario:,.2f}")
    st.metric("Fixos", f"R$ {fixos:,.2f}")
    st.metric("Variáveis", f"R$ {variaveis:,.2f}")
    st.metric("Total Gastos", f"R$ {total:,.2f}")
    st.metric("Saldo", f"R$ {saldo:,.2f}", delta_color="normal" if saldo >= 0 else "inverse")

    if salario > 0:
        percentual = (total / salario) * 100
        st.progress(min(percentual / 100, 1.0))
        st.write(f"**{percentual:.1f}%** do salário utilizado")

        if percentual > 100:
            st.error("⚠️ Gastos excedem o salário!")
        elif percentual > 80:
            st.warning("⚠️ Gastos elevados (acima de 80%)")
        else:
            st.success("✓ Gastos controlados")

    # --- Meta do mês ---
    meta_mes = obter_meta(selecionado)
    if meta_mes and meta_mes > 0:
        st.markdown("---")
        st.markdown("### 🎯 Meta do Mês")
        diferenca = meta_mes - total
        if diferenca >= 0:
            st.success(f"Dentro da meta! Resta R$ {diferenca:,.2f}")
        else:
            st.error(f"Meta ultrapassada em R$ {abs(diferenca):,.2f}")

# -------------------------
# Visualizações
# -------------------------
st.markdown("---")
st.subheader("📈 Visualizações")

tab1, tab2, tab3 = st.tabs(["Distribuição", "Categorias", "Evolução Mensal"])

with tab1:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fixos, variaveis, total = somar_por_tipo(selecionado)
        if total > 0:
            fig = grafico_pizza_tipo(fixos, variaveis)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem gastos para exibir o gráfico.")

    with col_g2:
        gastos_mes_chart = obter_gastos_mes(selecionado)
        if gastos_mes_chart:
            fig = grafico_pizza_categorias(gastos_mes_chart)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem gastos para exibir o gráfico.")

with tab2:
    gastos_mes_bar = obter_gastos_mes(selecionado)
    if gastos_mes_bar:
        col_bar, col_gauge = st.columns(2)
        with col_bar:
            fig = grafico_barras_categorias(gastos_mes_bar)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        with col_gauge:
            meta_mes = obter_meta(selecionado)
            if meta_mes and meta_mes > 0:
                _, _, total_mes = somar_por_tipo(selecionado)
                fig = grafico_meta_vs_gasto(total_mes, meta_mes, selecionado)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Defina uma meta na barra lateral para ver o indicador.")
    else:
        st.info("Adicione gastos para ver os gráficos de categorias.")

with tab3:
    totais = totais_mensais()
    if any(totais.values()):
        fig = grafico_evolucao_mensal(MESES, list(totais.values()), salario)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem gastos para exibir a evolução mensal.")

# -------------------------
# Resumo Anual
# -------------------------
st.markdown("---")
st.subheader("📊 Resumo Anual")
totais = totais_mensais()
metas = obter_todas_metas()

if any(totais.values()):
    dados_anuais = []
    for m in MESES:
        gasto = totais[m]
        saldo_m = salario - gasto
        meta_m = metas.get(m)
        dados_anuais.append({
            "Mês": m,
            "Gasto": f"R$ {gasto:,.2f}",
            "Saldo": f"R$ {saldo_m:,.2f}",
            "Meta": f"R$ {meta_m:,.2f}" if meta_m else "—",
            "Status": "✅" if (meta_m and gasto <= meta_m) else ("⚠️" if meta_m else "—"),
        })

    df_anual = pd.DataFrame(dados_anuais)
    st.dataframe(df_anual, use_container_width=True, hide_index=True)

    total_ano = sum(totais.values())
    col_ano1, col_ano2, col_ano3 = st.columns(3)
    col_ano1.metric("Gasto Anual", f"R$ {total_ano:,.2f}")
    col_ano2.metric("Receita Anual", f"R$ {salario * 12:,.2f}")
    saldo_anual = (salario * 12) - total_ano
    col_ano3.metric("Saldo Anual", f"R$ {saldo_anual:,.2f}")
else:
    st.info("Adicione gastos para ver o resumo anual.")

# Rodapé
st.markdown("---")
st.caption("💡 Dashboard Financeiro • Dados persistidos automaticamente no banco de dados local")
