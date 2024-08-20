import sqlite3

# Conectar ao banco de dados (cria o arquivo se não existir)
conn = sqlite3.connect('facial_recognition.db')
cursor = conn.cursor()

# Criar a tabela 'colaboradores' com os campos especificados
cursor.execute('''
CREATE TABLE IF NOT EXISTS colaboradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    funcao TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    imagem BLOB NOT NULL
)
''')

# Criar a tabela 'entradas' para registrar as entradas com data e hora
cursor.execute('''
CREATE TABLE IF NOT EXISTS entradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    funcao TEXT NOT NULL,
    cpf TEXT NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Salvar as alterações e fechar a conexão com o banco de dados
conn.commit()
conn.close()
