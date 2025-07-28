import streamlit as st
from app.database import registrar_venda, obter_vendas, obter_recebimentos, atualizar_venda, deletar_venda
from app.config import salvar_config
from app.layout import exibir_historico_vendas

def exibir_aba_vendas(config):
    st.subheader("🧾 Registrar Venda")

    # Campo para ajustar o valor unitário
    valor_unitario = st.number_input(
        "Valor do Saquinho (R$)",
        min_value=0.01,
        value=float(config["valor_unitario"]),
        step=0.10,
        format="%.2f",
        key="valor_unitario_input"
    )

    # Campo para quantidade vendida
    quantidade = st.number_input(
        "Quantidade Vendida (saquinhos)",
        min_value=1,
        step=1,
        format="%d",
        key="quantidade_input"
    )

    # Botão para registrar venda
    if st.button("Registrar Venda"):
        if quantidade > 0 and valor_unitario > 0:
            registrar_venda(quantidade, valor_unitario)
            salvar_config({"valor_unitario": valor_unitario})
            st.success(f"Venda registrada: {quantidade} saquinhos a R$ {valor_unitario:.2f} cada.")
        else:
            st.error("Preencha todos os campos corretamente.")

