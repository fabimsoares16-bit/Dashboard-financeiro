'''
Dashboard Financeiro Interativo Para Gestão Pessoal de Despesas.

Criar o ambiente virtual: python3 -m venv .venv

Ativar o ambiente virtual em Windows: .venv\Scripts\Activate

Ativar o ambiente virtual em MAC/LINUX: source .venv/bin/activate

Instalar as bibliotecas necessárias: pip install -r requirements.txt

Rodar a aplicação: streamlit run app.py
'''

# Importações principais
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import io

# Configurações iniciais da página Streamlit
st.set_page_config(layout="wide", page_title="Dashboard Financeiro", page_icon="💰")

# -------------------------
# Inicialização dos estados
# -------------------------
# Usamos st.session_state para persistir os dados (salário, mês selecionado, gastos)
if "salario" not in st.session_state:
    st.session_state.salario = 0.0  # salário mensal padrão

if "mes_selecionado" not in st.session_state:
    st.session_state.mes_selecionado = "Janeiro"  # mês inicialmente selecionado

if "gastos" not in st.session_state:
    st.session_state.gastos = []  # lista de gastos armazenados como dicionários

# Lista estática com os meses (ordem usada nos gráficos/tabelas)
MESES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

# -------------------------
# Funções utilitárias
# -------------------------
def obter_gastos_mes(mes):
    """
    Retorna a lista de gastos armazenados para o mês fornecido.

    Args:
        mes (str): Nome do mês (ex: "Janeiro").

    Returns:
        list: Lista de dicionários com gastos daquele mês.
    """
    return [g for g in st.session_state.gastos if g["mes"] == mes]

def somar_por_tipo(mes):
    """
    Soma os valores dos gastos do mês por tipo (Fixo/Variável).

    Args:
        mes (str): Nome do mês.

    Returns:
        tuple: (fixos, variaveis, total) — soma dos fixos, variáveis e total.
    """
    gastos = obter_gastos_mes(mes)
    fixos = sum(g["valor"] for g in gastos if g["tipo"] == "Fixo")
    variaveis = sum(g["valor"] for g in gastos if g["tipo"] == "Variável")
    return fixos, variaveis, fixos + variaveis

def totais_mensais():
    """
    Calcula o total de gastos para cada mês (usado para gráficos e resumo anual).

    Returns:
        dict: Mapeamento mês -> total_gastos.
    """
    return {m: somar_por_tipo(m)[2] for m in MESES}

def exportar_csv():
    """
    Gera um CSV com os gastos e o salário atual, retornando os bytes para download.

    Returns:
        bytes: Conteúdo CSV codificado em UTF-8.
    """
    df = pd.DataFrame(st.session_state.gastos)
    # Adiciona coluna salário para facilitar a restauração posterior (mesmo que repetida)
    df["salario"] = st.session_state.salario
    return df.to_csv(index=False).encode('utf-8')

def importar_csv(arquivo):
    """
    Importa um CSV enviado pelo usuário e popula st.session_state.gastos e salario.

    Args:
        arquivo: Arquivo tipo upload do Streamlit (io.BytesIO / UploadedFile)
    """
    try:
        df = pd.read_csv(arquivo)
        # Garante que a estrutura interna mantenha apenas as chaves necessárias
        st.session_state.gastos = df[["mes","tipo","descricao","valor"]].to_dict(orient="records")
        # Se o CSV tiver coluna 'salario', utiliza o primeiro valor (pressupõe consistência)
        if "salario" in df.columns:
            st.session_state.salario = float(df["salario"].iloc[0])
        st.success("Dados carregados!")
        st.rerun()  # reenfileira a execução para atualizar UI com dados importados
    except Exception as e:
        st.error(f"Erro: {e}")

# -------------------------
# Layout principal
# -------------------------
st.title("💰 Dashboard Financeiro")

# ---------- Sidebar (Configurações / Backup) ----------
with st.sidebar:
    st.header("⚙️ Configurações")
    # Input do salário mensal: atualiza diretamente st.session_state.salario
    st.session_state.salario = st.number_input(
        "Salário mensal (R$)",
        min_value=0.0,
        value=float(st.session_state.salario),
        step=100.0,
        format="%.2f"
    )
    
    st.markdown("---")
    st.subheader("💾 Backup")
    
    # Se houver gastos, permitir download do CSV gerado
    if st.session_state.gastos:
        st.download_button("⬇️ Baixar", exportar_csv(), "backup.csv", "text/csv")
    
    # Upload para restaurar backup CSV
    arquivo_enviado = st.file_uploader("⬆️ Restaurar", type=["csv"])
    # O botão "Carregar" garante que o usuário confirme a ação (evita carregamento automático)
    if arquivo_enviado and st.button("Carregar"):
        importar_csv(arquivo_enviado)
    
    st.markdown("---")
    # Botão para limpar todos os dados (gastos + salário)
    if st.button("🗑️ Limpar tudo"):
        st.session_state.gastos = []
        st.session_state.salario = 0.0
        st.rerun()

# ---------- Seleção de mês com botões ----------
st.subheader("📅 Selecione o Mês")
colunas = st.columns(4)  # organiza os meses em 4 colunas

for i, mes in enumerate(MESES):
    with colunas[i % 4]:
        # Somatório do mês para mostrar no botão/caption
        _, _, total = somar_por_tipo(mes)
        esta_selecionado = st.session_state.mes_selecionado == mes
        # Botões que mudam o mês selecionado; usamos key único por botão
        if st.button(
            f"{'✓ ' if esta_selecionado else ''}{mes}",
            key=f"btn_{mes}",
            type="primary" if esta_selecionado else "secondary",
            use_container_width=True
        ):
            st.session_state.mes_selecionado = mes
            st.rerun()
        # Pequena legenda com o total ou aviso de sem gastos
        st.caption(f"R$ {total:.2f}" if total > 0 else "Sem gastos")

st.markdown("---")

# ---------- Área principal dividida ----------
selecionado = st.session_state.mes_selecionado
st.subheader(f"📊 {selecionado}")
col1, col2 = st.columns([2,1])  # col1 maior para formulário e tabela; col2 para resumo

with col1:
    st.markdown("### ➖ Adicionar Gasto")
    # Formulário para adicionar um novo gasto no mês selecionado
    with st.form(key="formulario_adicionar", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["Fixo","Variável"])
        descricao = st.text_input("Descrição", placeholder="Ex: Aluguel, Conta de luz...")
        valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", step=10.0)
        
        # Ao submeter o formulário, validamos e armazenamos no session_state
        if st.form_submit_button("✅ Adicionar", use_container_width=True):
            if not descricao.strip():
                st.error("Preencha a descrição")
            elif valor <= 0:
                st.error("Valor deve ser maior que zero")
            else:
                st.session_state.gastos.append({
                    "mes": selecionado,
                    "tipo": tipo,
                    "descricao": descricao,
                    "valor": valor
                })
                st.success(f"{tipo} adicionado: {descricao} — R$ {valor:.2f}")
                st.rerun()

    st.markdown("### 📋 Gastos Cadastrados")
    gastos_mes = obter_gastos_mes(selecionado)
    
    if not gastos_mes:
        st.info("Nenhum gasto cadastrado")
    else:
        # Exibe uma tabela com tipos, descrições e valores formatados
        df = pd.DataFrame(gastos_mes)[["tipo", "descricao", "valor"]]
        df.columns = ["Tipo", "Descrição", "Valor"]
        df["Valor"] = df["Valor"].apply(lambda x: f"R$ {x:.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Fornece uma selectbox para escolher um item a remover (índice + descrição)
        opcoes = ["Selecione..."] + [f'{i+1}. {g["descricao"]} - R$ {g["valor"]:.2f}' for i, g in enumerate(gastos_mes)]
        para_remover = st.selectbox("Remover", opcoes, label_visibility="collapsed")
        
        # Ação de remoção: converte a string selecionada em índice e remove da lista global
        if st.button("🗑️ Remover", disabled=(para_remover == opcoes[0])):
            indice = int(para_remover.split(".")[0]) - 1
            # Remove do estado (atenção: gastos_mes é uma fatia; removendo pela referência na lista principal)
            st.session_state.gastos.remove(gastos_mes[indice])
            st.success("Removido!")
            st.rerun()

with col2:
    st.markdown("### 💵 Resumo")
    # Calcula somatórios para o mês selecionado
    fixos, variaveis, total = somar_por_tipo(selecionado)
    salario = st.session_state.salario
    saldo = salario - total
    
    # Mostra métricas principais
    st.metric("Salário", f"R$ {salario:.2f}")
    st.metric("Fixos", f"R$ {fixos:.2f}")
    st.metric("Variáveis", f"R$ {variaveis:.2f}")
    st.metric("Total Gastos", f"R$ {total:.2f}")
    # Usa cor normal se saldo >= 0, inverse (vermelho) caso negativo
    st.metric("Saldo", f"R$ {saldo:.2f}", delta_color="normal" if saldo >= 0 else "inverse")

    # Se salário informado, mostramos progresso percentual e avisos
    if salario > 0:
        percentual = (total / salario) * 100
        st.progress(min(percentual / 100, 1.0))
        st.write(f"**{percentual:.1f}%** do salário")
        
        # Mensagens de alerta conforme o percentual de gasto
        if percentual > 100:
            st.error("⚠️ Gastos excedem salário!")
        elif percentual > 80:
            st.warning("⚠️ Gastos altos")
        else:
            st.success("✓ Gastos controlados")

# -------------------------
# Gráficos / Visualizações
# -------------------------
st.markdown("---")
st.subheader("📈 Visualizações")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.markdown(f"**Distribuição - {selecionado}**")
    fixos, variaveis, total = somar_por_tipo(selecionado)
    
    if total > 0:
        # Prepara DataFrame para o gráfico de pizza (percentual por tipo)
        distribuicao_contagem = pd.DataFrame({"tipo": ["Fixos","Variáveis"], "quantidade": [fixos, variaveis]})
        distribuicao_contagem.columns = ["tipo","quantidade"]
        fig = px.pie(
            distribuicao_contagem,
            names='tipo',
            values='quantidade',
            title="Distribuição dos Gastos",
            color_discrete_sequence=['#ff6b6b', '#4ecdc4']
        )
        # Mostrar percentuais + rótulo
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem gastos")

with col_graf2:
    st.markdown("**Evolução Mensal**")
    totais = totais_mensais()
    
    # Se houver qualquer gasto no ano, plota uma linha com os totais por mês
    if any(totais.values()):
        fig = px.line(
            x=MESES,
            y=list(totais.values()),
            title="Gastos Mensais",
            labels={'x': 'Mês', 'y': 'Total (R$)'},
            color_discrete_sequence=['#4ecdc4'],
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem gastos")

# -------------------------
# Resumo Anual
# -------------------------
st.markdown("---")
st.subheader("📊 Resumo Anual")
totais = totais_mensais()

if any(totais.values()):
    # Monta DataFrame com Gasto e Saldo por mês (formatado)
    df = pd.DataFrame([{"Mês": m, "Gasto": totais[m], "Saldo": salario - totais[m]} for m in MESES])
    df["Gasto"] = df["Gasto"].apply(lambda x: f"R$ {x:.2f}")
    df["Saldo"] = df["Saldo"].apply(lambda x: f"R$ {x:.2f}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Métricas agregadas anuais
    total_ano = sum(totais.values())
    col_ano1, col_ano2, col_ano3 = st.columns(3)
    col_ano1.metric("Gasto Anual", f"R$ {total_ano:.2f}")
    col_ano2.metric("Receita Anual", f"R$ {salario * 12:.2f}")
    col_ano3.metric("Saldo Anual", f"R$ {(salario * 12) - total_ano:.2f}")
else:
    st.info("Adicione gastos para ver o resumo")

# Rodapé
st.caption("💡 Desenvolvido com Streamlit • Use backup para não perder dados")