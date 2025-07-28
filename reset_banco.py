import sqlite3
import sys
from app.database import conectar  # Supondo que você tenha uma função de conexão em `app.database`

def resetar_banco_completo():
    """
    Função para resetar completamente o banco de dados:
    - Deletar todos os dados das tabelas.
    - Reiniciar os IDs das tabelas.
    """
    # Conectar ao banco de dados
    conn = conectar()
    cursor = conn.cursor()

    # Deletar todos os dados das tabelas
    cursor.execute("DELETE FROM vendas")
    cursor.execute("DELETE FROM gastos")
    cursor.execute("DELETE FROM recebimentos")

    # Reiniciar os IDs (para garantir que comecem do 1 novamente)
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'vendas'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'gastos'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'recebimentos'")

    # Commit e fechamento da conexão
    conn.commit()
    conn.close()

    print("Banco de dados resetado com sucesso!")

if __name__ == "__main__":
    # Verifica se o argumento de confirmação foi passado
    if len(sys.argv) > 1 and sys.argv[1].lower() == "sim":
        resetar_banco_completo()
    else:
        print("Para resetar o banco de dados, execute o script com o argumento 'sim' para confirmação.")
        print("Exemplo: python reset_banco.py SIM")
