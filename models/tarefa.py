from models.database import Database
from typing import Self, Any, Optional
from sqlite3 import Cursor

class Tarefa:
    def __init__(self: Self, titulo_tarefa: Optional[str], data_conclusao: Optional[str] = None, id_tarefa: Optional[int] = None) -> None:
        self.titulo_tarefa = titulo_tarefa
        self.data_conclusao = data_conclusao
        self.id_tarefa = id_tarefa

    @classmethod
    def id(cls, id: int) -> Self:
        with Database('./data/tarefas.sqlite3') as db:
            query = 'SELECT titulo_tarefa, data_conclusao FROM tarefas WHERE id = ?;'
            params = (id,)
            [[titulo, data]] = db.buscar_tudo(query, params)
        return cls(titulo, data, id)

    def salvar_tarefa(self) -> None:
        with Database('./data/tarefas.sqlite3') as db:
            query = "INSERT INTO tarefas (titulo_tarefa, data_conclusao) VALUES (?, ?);"
            params = (self.titulo_tarefa, self.data_conclusao)
            db.executar(query, params)

    @classmethod
    def obter_tarefas(cls) -> list[Self]:
        with Database('./data/tarefas.sqlite3') as db:
            query = 'SELECT titulo_tarefa, data_conclusao, id FROM tarefas;'
            resultados = db.buscar_tudo(query)
            return [cls(titulo, data, id) for titulo, data, id in resultados]

    def excluir_tarefa(self) -> None:
        with Database('./data/tarefas.sqlite3') as db:
            query = 'DELETE FROM tarefas WHERE id = ?;'
            db.executar(query, (self.id_tarefa,))

    def atualizar_tarefa(self) -> Cursor:
        with Database('./data/tarefas.sqlite3') as db:
            query: str = 'UPDATE tarefas SET titulo_tarefa = ?, data_conclusao = ? WHERE id = ?;'
            params: tuple = ( self.titulo_tarefa, self.data_conclusao, self.id_tarefa )
            resultado: Cursor = db.executar(query, params)
            return resultado
