import streamlit as st
from app.database import registrar_recebimento, obter_recebimentos, deletar_recebimento, atualizar_recebimento
from app.layout import exibir_historico_recebimentos

def exibir_aba_recebido():
    st.subheader("💵 Registrar Recebimento")

    # Campo para valor recebido
    valor = st.number_input(
        "Valor Recebido (R$)",
        min_value=0.01,
        step=0.50,
        format="%.2f",
        key="valor_recebido_input"
    )

    if st.button("Registrar Recebimento"):
        if valor > 0:
            registrar_recebimento(valor)
            st.success(f"Recebimento de R$ {valor:.2f} registrado com sucesso!")
        else:
            st.error("Informe um valor válido.")

    # Mostrar total recebido até o momento
    dados = obter_recebimentos()
    total = sum(r[2] for r in dados) if dados else 0
    st.info(f"Total Recebido até agora: R$ {total:.2f}")
