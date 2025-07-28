import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
from app.database import obter_vendas, atualizar_venda, deletar_venda, deletar_recebimento, deletar_gasto

# ------------------ INICIALIZAÇÃO DO SESSION_STATE ------------------

# Inicializa as variáveis no session_state se não existirem
if "gastos" not in st.session_state:
    st.session_state.gastos = []  # Ou inicialize com os dados que deseja
if "vendas" not in st.session_state:
    st.session_state.vendas = []  # Ou inicialize com os dados que deseja
if "recebimentos" not in st.session_state:
    st.session_state.recebimentos = []  # Ou inicialize com os dados que deseja
if "aba" not in st.session_state:
    st.session_state["aba"] = "graficos"  # Inicializa com a aba padrão

# ------------------ LOGO + ABAS ------------------

def exibir_abas_com_logo(aba_atual):
    if "aba" not in st.session_state:
        st.session_state["aba"] = aba_atual

    col_logo, col_abas = st.columns([1, 5])
    
    # Exibe a logo na coluna da esquerda
    with col_logo:
        logo_path = Path(__file__).parents[1] / "logo.webp"
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                img_bytes = f.read()
            st.image(img_bytes, width=180)

    # Botões centralizados ao lado da logo
    with col_abas:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            if st.button("Gráficos"):
                st.session_state["aba"] = "graficos"
        with col2:
            if st.button("Gastos"):
                st.session_state["aba"] = "gastos"
        with col3:
            if st.button("Vendas"):
                st.session_state["aba"] = "vendas"
        with col4:
            if st.button("Recebido"):
                st.session_state["aba"] = "recebido"

    return st.session_state["aba"]

# ------------------ GRÁFICO ------------------

def exibir_grafico_vendas_gastos(vendas, gastos):
    st.subheader("📊 Evolução de Vendas vs Gastos")

    df_vendas = pd.DataFrame(vendas, columns=["id", "data_hora", "quantidade", "valor_unitario", "valor_total"])
    df_gastos = pd.DataFrame(gastos, columns=["id", "data_hora", "tipo", "quantidade", "valor"])

    if df_vendas.empty and df_gastos.empty:
        st.info("Ainda não há dados suficientes para exibir o gráfico.")
        return

    df_vendas["data"] = pd.to_datetime(df_vendas["data_hora"]).dt.date
    df_gastos["data"] = pd.to_datetime(df_gastos["data_hora"]).dt.date

    vendas_por_dia = df_vendas.groupby("data")["valor_total"].sum().reset_index(name="Vendas")
    gastos_por_dia = df_gastos.groupby("data")["valor"].sum().reset_index(name="Gastos")

    df_merged = pd.merge(vendas_por_dia, gastos_por_dia, on="data", how="outer").fillna(0)
    df_merged = df_merged.sort_values("data")

    # Converte data para string formatada "dd/mm/yyyy"
    df_merged["data"] = df_merged["data"].apply(lambda x: x.strftime("%d/%m/%Y"))

    fig = px.line(
        df_merged,
        x="data",
        y=["Vendas", "Gastos"],
        markers=True,
        labels={
            "value": "Valor (R$)",
            "variable": "Categoria",
            "data": "Data"
        }
    )

    fig.update_layout(legend_title_text="Categoria")
    st.plotly_chart(fig, use_container_width=True)

# ------------------ RESUMO ------------------

def exibir_resumo_financeiro(vendas, gastos, recebimentos):
    st.subheader("📌 Resumo Financeiro do Mês")

    total_vendas = sum(v[4] for v in vendas) if vendas else 0
    total_gastos = sum(g[4] for g in gastos) if gastos else 0
    total_recebido = sum(r[2] for r in recebimentos) if recebimentos else 0
    saldo = total_recebido - total_gastos

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Vendido", f"R$ {total_vendas:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
    col2.metric("💵 Total Recebido", f"R$ {total_recebido:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
    col3.metric("📦 Total de Gastos", f"R$ {total_gastos:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
    col4.metric("📈 Saldo", f"R$ {saldo:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

# ------------------ HISTÓRICO DE VENDAS ------------------

def exibir_historico_vendas(vendas, recebimentos):
    df_vendas = pd.DataFrame(vendas, columns=["id", "data_hora", "quantidade", "valor_unitario", "valor_total"])
    df_recebido = pd.DataFrame(recebimentos, columns=["id", "data_hora", "valor_recebido"])

    if df_vendas.empty:
        st.info("Nenhuma venda registrada ainda.")
        return

    total_recebido = df_recebido["valor_recebido"].sum() if not df_recebido.empty else 0
    df_vendas["valor_recebido"] = 0.0
    df_vendas["valor_a_receber"] = 0.0

    valor_faltante = total_recebido
    for i in df_vendas.index:
        venda_total = df_vendas.at[i, "valor_total"]
        recebido = min(valor_faltante, venda_total)
        df_vendas.at[i, "valor_recebido"] = recebido
        df_vendas.at[i, "valor_a_receber"] = venda_total - recebido
        valor_faltante -= recebido
        if valor_faltante <= 0:
            break

    st.header("📋 Histórico de Vendas")

    for _, row in df_vendas.iterrows():
        pago = row["valor_a_receber"] <= 0.01
        cor_fundo = "#D4EDDA" if pago else "#F8D7DA"
        venda_id = row["id"]

        st.markdown(
            f"""
            <div style="
                background-color:{cor_fundo};
                padding:10px;
                border-radius:5px;
                margin-bottom:5px;
                color:#000;
                font-size:15px;
            ">
                <strong>ID:</strong> {venda_id} |
                <strong>Data:</strong> {row['data_hora']} |
                <strong>Qtd:</strong> {row['quantidade']} |
                <strong>Recebido:</strong> R$ {row['valor_recebido']:.2f} |
                <strong>A Receber:</strong> R$ {row['valor_a_receber']:.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander(f"Editar venda ID {venda_id}"):
            with st.form(f"form_editar_{venda_id}", clear_on_submit=False):
                nova_qtde = st.number_input("Nova quantidade", value=float(row["quantidade"]), min_value=0.0, step=1.0)
                novo_valor = st.number_input("Novo valor unitário (R$)", value=float(row["valor_unitario"]), min_value=0.0, step=0.1, format="%.2f")
                submitted = st.form_submit_button("Salvar alterações")

                if submitted:
                    atualizar_venda(venda_id, nova_qtde, novo_valor)
                    st.success("✅ Venda atualizada com sucesso!")

            if st.button("Excluir venda", key=f"excluir_venda_{venda_id}"):
                deletar_venda(venda_id)
                st.success(f"🗑️ Venda {venda_id} excluída com sucesso!")
                # Atualizar o estado para garantir que os dados sejam atualizados
                st.session_state.vendas = [v for v in st.session_state.vendas if v["id"] != venda_id]  # Atualiza as vendas

# ------------------ HISTÓRICO DE RECEBIMENTOS ------------------

def exibir_historico_recebimentos(recebimentos):
    if not recebimentos:
        st.info("Nenhum recebimento registrado ainda.")
        return

    # Criação do dataframe com os dados de recebimentos
    df_recebimentos = pd.DataFrame(recebimentos, columns=["id", "data_hora", "valor_recebido"])

    # --- Calcular o total de vendas ---
    vendas = obter_vendas()  # Obtém as vendas
    total_vendas = sum(v[4] for v in vendas)  # Soma o valor total das vendas

    # Exibe o cabeçalho do histórico de recebimentos
    st.header("📋 Histórico de Recebimentos")

    # --- Calcular o total de recebimentos até o momento ---
    total_recebido = df_recebimentos["valor_recebido"].sum()

    # --- Verificar a situação de pagamento ---
    if total_recebido < total_vendas:
        cor = "red"  # Cor vermelha se o total recebido for menor que o total de vendas
        status_pagamento = f"Falta R$ {total_vendas - total_recebido:.2f} para quitar a dívida."
    else:
        cor = "green"  # Cor verde se o total de recebimentos for igual ao total de vendas
        status_pagamento = "Dívida quitada!"

    # --- Loop para exibir os recebimentos ---
    for _, row in df_recebimentos.iterrows():
        receb_id = row["id"]
        valor_recebido = row["valor_recebido"]

        # Exibe o recebimento com a cor condicional
        st.markdown(
            f"""
            <div style="
                background-color:#D1ECF1;
                padding:10px;
                border-radius:5px;
                margin-bottom:5px;
                color:{cor};  /* Cor dinâmica baseada no status de pagamento */
                font-size:15px;
            ">
                <strong>ID:</strong> {receb_id} |
                <strong>Data:</strong> {row['data_hora']} |
                <strong>Valor:</strong> R$ {valor_recebido:.2f} |
                <strong>Status:</strong> {status_pagamento}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Botão para excluir o recebimento
        if st.button("Excluir recebimento", key=f"excluir_receb_{receb_id}"):
            deletar_recebimento(receb_id)
            st.success(f"🗑️ Recebimento {receb_id} excluído com sucesso!")
            # Atualiza o estado para garantir que os dados sejam atualizados
            st.session_state.recebimentos = [r for r in st.session_state.recebimentos if r["id"] != receb_id]

# ------------------ HISTÓRICO DE GASTOS ------------------

def exibir_historico_gastos(gastos):
    # Verifique se há dados em gastos
    if not gastos:
        st.info("Nenhum gasto registrado ainda.")
        return

    # Converte para DataFrame para exibição
    df_gastos = pd.DataFrame(gastos, columns=["id", "data_hora", "tipo", "quantidade", "valor"])

    # Exibe o cabeçalho
    st.header("📋 Histórico de Gastos")

    # Loop para exibir cada registro de gasto
    for _, row in df_gastos.iterrows():
        gasto_id = row["id"]
        st.markdown(
            f"""
            <div style="
                background-color:#FCE5CD;
                padding:10px;
                border-radius:5px;
                margin-bottom:5px;
                color:#000;
                font-size:15px;
            ">
                <strong>ID:</strong> {gasto_id} |
                <strong>Data:</strong> {row['data_hora']} |
                <strong>Tipo:</strong> {row['tipo']} |
                <strong>Qtd:</strong> {row['quantidade']} |
                <strong>Valor:</strong> R$ {row['valor']:.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Botão para excluir o gasto
        if st.button(f"Excluir gasto {gasto_id}", key=f"excluir_gasto_{gasto_id}"):
            deletar_gasto(gasto_id)
            st.success(f"🗑️ Gasto {gasto_id} excluído com sucesso!")
            # Atualizar o estado de sessão para garantir que os dados sejam atualizados
            st.session_state.gastos = [g for g in st.session_state.gastos if g["id"] != gasto_id]  # Atualiza a lista de gastos
