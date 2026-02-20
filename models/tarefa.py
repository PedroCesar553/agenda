from models.database import Database
from datetime import datetime

class Tarefa:
    def __init__(self, titulo_tarefa, data_conclusao=None, id_tarefa=None, concluida=0, data_hora_conclusao=None):
        self.titulo_tarefa = titulo_tarefa
        self.data_conclusao = data_conclusao
        self.id_tarefa = id_tarefa
        self.concluida = concluida
        self.data_hora_conclusao = data_hora_conclusao

    @classmethod
    def id(cls, id_procurado):
        with Database() as db:
            query = 'SELECT titulo_tarefa, data_conclusao, concluida, data_hora_conclusao FROM tarefas WHERE id = ?;'
            resultado = db.buscar_tudo(query, (id_procurado,))
            
            if not resultado:
                return None
                
            titulo, data, concluida, data_hora = resultado[0]
            return cls(titulo_tarefa=titulo, data_conclusao=data, id_tarefa=id_procurado, 
                       concluida=concluida, data_hora_conclusao=data_hora)

    @classmethod
    def obter_tarefas(cls):
        with Database() as db:
            query = 'SELECT titulo_tarefa, data_conclusao, id, concluida, data_hora_conclusao FROM tarefas;'
            resultados = db.buscar_tudo(query)
            return [cls(t, d, i, c, dh) for t, d, i, c, dh in resultados]

    def salvar_tarefa(self):
        with Database() as db:
            query = "INSERT INTO tarefas (titulo_tarefa, data_conclusao, concluida) VALUES (?, ?, 0);"
            db.executar(query, (self.titulo_tarefa, self.data_conclusao))

    def alternar_conclusao(self):
        novo_estado = 1 if self.concluida == 0 else 0
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S") if novo_estado == 1 else None
        with Database() as db:
            query = 'UPDATE tarefas SET concluida = ?, data_hora_conclusao = ? WHERE id = ?;'
            db.executar(query, (novo_estado, agora, self.id_tarefa))
        return novo_estado, agora

    def excluir_tarefa(self):
        if self.concluida == 1: # RN01: Não exclui concluídas
            return False
        with Database() as db:
            query = 'DELETE FROM tarefas WHERE id = ?;'
            db.executar(query, (self.id_tarefa,))
            return True

    def atualizar_tarefa(self):
        with Database() as db:
            query = 'UPDATE tarefas SET titulo_tarefa = ?, data_conclusao = ? WHERE id = ?;'
            db.executar(query, (self.titulo_tarefa, self.data_conclusao, self.id_tarefa))