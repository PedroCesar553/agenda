from models.database import Database
from typing import Optional, Self, Any
from sqlite3 import Cursor


class Tarefa:
    """
      Classe para representar uma tarefa, com metodos para salvar, obter,
      excluir e atualizar tarefas em um banco de dados
      usando a classe 'Database'.
    """

    def __init__(
        self: Self,
        titulo_tarefa: Optional[str],
        data_conclusao: Optional[str] = None,
        id_tarefa: Optional[int] = None,
    ) -> None:
        self.titulo_tarefa: Optional[str] = titulo_tarefa
        self.data_conclusao: Optional[str] = data_conclusao
        self.id_tarefa: Optional[int] = id_tarefa

    @classmethod
    def id(cls, id_procurado):
        with Database() as db:
            query: str = (
                "SELECT titulo_tarefa, data_conclusao FROM tarefas WHERE id = ?;"
            )
            params: tuple = (id_procurado,)
            resultado: list[Any] = db.buscar_tudo(query, params)

            [[titulo, data]] = resultado

        return cls(id_tarefa=id_procurado, titulo_tarefa=titulo, data_conclusao=data)

    def salvar_tarefa(self: Self) -> None:
        with Database() as db:
            query: str = (
                "INSERT INTO tarefas (titulo_tarefa, data_conclusao) VALUES (?, ?);"
            )
            params: tuple = (self.titulo_tarefa, self.data_conclusao)
            db.executar(query, params)

    @classmethod
    def obter_tarefas(cls):
        with Database() as db:
            query = 'SELECT titulo_tarefa, data_conclusao, id, concluida, data_hora_conclusao FROM tarefas;'
            resultados = db.buscar_tudo(query)
            return [cls(t, d, i) for t, d, i, c, dh in resultados]

    def excluir_tarefa(self) -> Cursor:
        with Database() as db:
            query: str = "DELETE FROM tarefas WHERE id = ?;"
            params: tuple = (self.id_tarefa,)
            resultado: Cursor = db.executar(query, params)
            return resultado

    def atualizar_tarefa(self) -> Cursor:
        with Database() as db:
            query: str = (
                "UPDATE tarefas SET titulo_tarefa = ?, data_conclusao = ? WHERE id = ?;"
            )
            params: tuple = (self.titulo_tarefa, self.data_conclusao, self.id_tarefa)
            resultado: Cursor = db.executar(query, params)
            return resultado