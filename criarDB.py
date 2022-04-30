import sqlite3

# conectando...
conn = sqlite3.connect('EstufaDB.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE humid (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        humid INTEGER,
        datahumid DATETIME
);
""")

cursor.execute("""
CREATE TABLE dht11 (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        temp INTEGER,
        humid INTEGER,
        datadht11 DATETIME
);
""")

cursor.execute("""
CREATE TABLE reserv (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        reserv INTEGER,
        datareserv DATETIME
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()