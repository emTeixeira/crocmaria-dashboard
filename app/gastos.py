import streamlit as st
from app.database import registrar_gasto, obter_gastos, atualizar_gasto, deletar_gasto
from app.layout import exibir_historico_gastos


def exibir_aba_gastos():
    st.subheader("📉 Registrar Gastos")

    # Cria 7 colunas: 4 para inputs e 3 para as linhas verticais
    col1, line1, col2, line2, col3, line3, col4 = st.columns([10, 1, 10, 1, 10, 1, 10])

    linha_vertical_html = """
    <div style="
        border-left: 1px solid #ccc;
        height: 150px;  /* ajuste conforme altura dos inputs */
        margin: 0 auto;
    "></div>
    """

    with col1:
        st.markdown("### Amendoim")
        amendoim_valor = st.number_input("Valor (R$) - Amendoim", min_value=0.0, step=0.10, format="%.2f", key="amendoim_valor")
        amendoim_kg = st.number_input("Quantidade (Kg) - Amendoim", min_value=0.0, step=0.1, format="%.2f", key="amendoim_kg")
        if st.button("Registrar gasto com Amendoim", key="btn_amendoim"):
            if amendoim_valor > 0 and amendoim_kg > 0:
                registrar_gasto("Amendoim", amendoim_kg, amendoim_valor)
                st.success(f"Gasto Amendoim registrado: {amendoim_kg} Kg por R$ {amendoim_valor:.2f}")
            else:
                st.error("Informe valores válidos para Amendoim.")

    with line1:
        st.markdown(linha_vertical_html, unsafe_allow_html=True)

    with col2:
        st.markdown("### Açúcar")
        acucar_valor = st.number_input("Valor (R$) - Açúcar", min_value=0.0, step=0.10, format="%.2f", key="acucar_valor")
        acucar_kg = st.number_input("Quantidade (Kg) - Açúcar", min_value=0.0, step=0.1, format="%.2f", key="acucar_kg")
        if st.button("Registrar gasto com Açúcar", key="btn_acucar"):
            if acucar_valor > 0 and acucar_kg > 0:
                registrar_gasto("Açúcar", acucar_kg, acucar_valor)
                st.success(f"Gasto Açúcar registrado: {acucar_kg} Kg por R$ {acucar_valor:.2f}")
            else:
                st.error("Informe valores válidos para Açúcar.")

    with line2:
        st.markdown(linha_vertical_html, unsafe_allow_html=True)

    with col3:
        st.markdown("### Saquinhos")
        saquinho_valor = st.number_input("Valor (R$) - Saquinhos", min_value=0.0, step=0.10, format="%.2f", key="saquinho_valor")
        saquinho_qtde = st.number_input("Quantidade - Saquinhos", min_value=0, step=1, format="%d", key="saquinho_qtde")
        if st.button("Registrar gasto com Saquinhos", key="btn_saquinhos"):
            if saquinho_valor > 0 and saquinho_qtde > 0:
                registrar_gasto("Saquinhos", saquinho_qtde, saquinho_valor)
                st.success(f"Gasto Saquinhos registrado: {saquinho_qtde} unidades por R$ {saquinho_valor:.2f}")
            else:
                st.error("Informe valores válidos para Saquinhos.")

    with line3:
        st.markdown(linha_vertical_html, unsafe_allow_html=True)

    with col4:
        st.markdown("### Gás")
        gas_valor = st.number_input("Valor (R$) - Gás", min_value=0.0, step=0.10, format="%.2f", key="gas_valor")
        if st.button("Registrar gasto com Gás", key="btn_gas"):
            if gas_valor > 0:
                registrar_gasto("Gás", 0, gas_valor)
                st.success(f"Gasto Gás registrado: R$ {gas_valor:.2f}")
            else:
                st.error("Informe um valor válido para Gás.")

