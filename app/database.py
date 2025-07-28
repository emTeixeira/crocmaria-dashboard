import sqlite3
from datetime import datetime
from pathlib import Path
from app.config import caminho_banco  # Importa o caminho correto do banco

DB_PATH = caminho_banco  # Usa o caminho configurado no config.py

# ------------------ CONEXÃO ------------------
def conectar():
    return sqlite3.connect(DB_PATH)

# ------------------ INICIALIZAÇÃO ------------------
def inicializar_banco():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Garante que a pasta exista
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de vendas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            quantidade INTEGER,
            valor_unitario REAL,
            valor_total REAL
        )
    """)

    # Tabela de recebimentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recebimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            valor_recebido REAL
        )
    """)

    # Tabela de gastos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            tipo TEXT,
            quantidade REAL,
            valor REAL
        )
    """)

    conn.commit()
    conn.close()

# ------------------ INSERÇÕES ------------------
def registrar_venda(quantidade, valor_unitario):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    valor_total = quantidade * valor_unitario

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vendas (data_hora, quantidade, valor_unitario, valor_total)
        VALUES (?, ?, ?, ?)
    """, (data_hora, quantidade, valor_unitario, valor_total))
    conn.commit()
    conn.close()

def registrar_recebimento(valor_recebido):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO recebimentos (data_hora, valor_recebido)
        VALUES (?, ?)
    """, (data_hora, valor_recebido))
    conn.commit()
    conn.close()

def registrar_gasto(tipo, quantidade, valor):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO gastos (data_hora, tipo, quantidade, valor)
        VALUES (?, ?, ?, ?)
    """, (data_hora, tipo, quantidade, valor))
    conn.commit()
    conn.close()

# ------------------ CONSULTAS ------------------
def obter_vendas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendas ORDER BY data_hora DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def obter_recebimentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recebimentos ORDER BY data_hora DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados if dados else []

def obter_gastos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gastos ORDER BY data_hora DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

# ------------------ CÁLCULO FINANCEIRO ------------------
def calcular_valores_a_receber():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor_total) FROM vendas")
    total_vendas = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(valor_recebido) FROM recebimentos")
    total_recebido = cursor.fetchone()[0] or 0

    conn.close()
    return round(total_vendas - total_recebido, 2)

# ------------------ ATUALIZAÇÃO DE HISTÓRICO DE GASTOS ------------------

def atualizar_gasto(id_gasto, novo_tipo, nova_quantidade, novo_valor):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE gastos
            SET tipo = ?, quantidade = ?, valor = ?
            WHERE id = ?
            """,
            (novo_tipo, nova_quantidade, novo_valor, id_gasto)
        )
        conn.commit()

def deletar_gasto(id_gasto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gastos WHERE id = ?", (id_gasto,))
    conn.commit()
    conn.close()


# ------------------ ATUALIZAÇÃO DE HISTÓRICO DE VENDA ------------------
def atualizar_venda(id_venda, nova_qtde, novo_valor_unitario):
    novo_total = nova_qtde * novo_valor_unitario
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE vendas
            SET quantidade = ?, valor_unitario = ?, valor_total = ?
            WHERE id = ?
            """,
            (nova_qtde, novo_valor_unitario, novo_total, id_venda)
        )
        conn.commit()

def deletar_venda(id_venda):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vendas WHERE id = ?", (id_venda,))
        conn.commit()

# ------------------ ATUALIZAÇÃO DE HISTÓRICO DE RECEBIMENTO ------------------
def atualizar_recebimento(id_recebimento, novo_valor):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE recebimentos
            SET valor_recebido = ?
            WHERE id = ?
            """,
            (novo_valor, id_recebimento)
        )
        conn.commit()

def deletar_recebimento(id_recebimento):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recebimentos WHERE id = ?", (id_recebimento,))
        conn.commit()

