from sqlite3 import Connection, connect, Cursor
from typing import Any
from dotenv import load_dotenv
import traceback
import os

load_dotenv()
DB_PATH = os.getenv('DATABASE', './data/tarefas.sqlite3')

def init_db(db_name: str = DB_PATH) -> None:
    # Cria a pasta data se não existir para evitar erros
    os.makedirs(os.path.dirname(db_name), exist_ok=True)
    with connect(db_name) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_tarefa TEXT NOT NULL,
            data_conclusao TEXT,
            concluida INTEGER DEFAULT 0,
            data_hora_conclusao TEXT
        );
        """)

class Database:
    def __init__(self, db_name: str = DB_PATH) -> None:
        self.connection: Connection = connect(db_name)
        self.cursor: Cursor = self.connection.cursor()

    def executar(self, query: str, params: tuple = ()) -> Cursor:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor
    
    def buscar_tudo(self, query: str, params: tuple = ()) -> list[Any]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self) -> None:
        self.connection.close()

    # Simplificamos o gerenciador de contexto para remover avisos de tipos complexos
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb) -> None:
        if exc_type is not None:
            traceback.print_tb(tb)
        self.close()