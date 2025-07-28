import streamlit as st

from app.config import carregar_config
from app.database import inicializar_banco, obter_vendas, obter_gastos, obter_recebimentos
from app.layout import exibir_abas_com_logo, exibir_grafico_vendas_gastos, exibir_resumo_financeiro
from app.vendas import exibir_aba_vendas, exibir_historico_vendas
from app.gastos import exibir_historico_gastos, exibir_aba_gastos
from app.recebido import exibir_aba_recebido, exibir_historico_recebimentos

# Inicializa banco e tabelas (se ainda não existirem)
inicializar_banco()

# Carrega configurações (ex: valor unitário)
config = carregar_config()

# Inicializa a aba ativa no session_state se não existir
if "aba" not in st.session_state:
    st.session_state["aba"] = "vendas"  # aba padrão

# Exibe logo + abas como botões e atualiza a aba ativa
aba_atual = exibir_abas_com_logo(st.session_state["aba"])
st.session_state["aba"] = aba_atual  # sincroniza

# --- Obtém dados comuns para resumo financeiro
vendas = obter_vendas()
gastos = obter_gastos()
recebimentos = obter_recebimentos()

# --- Exibe o resumo financeiro antes de qualquer conteúdo específico
exibir_resumo_financeiro(vendas, gastos, recebimentos)

# --- Exibe o conteúdo específico da aba com seus respectivos históricos integrados
if aba_atual == "vendas":
    exibir_aba_vendas(config)
    st.markdown("---")
    exibir_historico_vendas(vendas, recebimentos)  # Exibe histórico de vendas

elif aba_atual == "gastos":
    exibir_aba_gastos()
    st.markdown("---")
    exibir_historico_gastos(gastos)  # Exibe histórico de gastos

elif aba_atual == "recebido":
    exibir_aba_recebido()
    st.markdown("---")
    exibir_historico_recebimentos(recebimentos)  # Exibe histórico de recebimentos

elif aba_atual == "graficos":
    exibir_grafico_vendas_gastos(vendas, gastos)

else:
    st.error("Aba inválida selecionada.")
