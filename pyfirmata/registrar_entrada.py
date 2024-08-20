import sqlite3
from datetime import datetime

def registrar_entrada(nome, funcao, cpf):
    # Conectar ao banco de dados
    conn = sqlite3.connect('facial_recognition.db')
    cursor = conn.cursor()

    # Inserir o registro de entrada na tabela
    cursor.execute('''
        INSERT INTO entradas (nome, funcao, cpf, data_hora)
        VALUES (?, ?, ?, ?)
    ''', (nome, funcao, cpf, datetime.now()))

    # Salvar as alterações e fechar a conexão
    conn.commit()
    conn.close()

# Exemplo de uso
nome = 'João Silva'
funcao = 'Analista'
cpf = '123.456.789-00'

registrar_entrada(nome, funcao, cpf)
