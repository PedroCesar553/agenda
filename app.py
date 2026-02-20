from flask import Flask, render_template, request, redirect, url_for, jsonify
from models.tarefa import Tarefa
from models.database import init_db

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    return redirect(url_for('agenda'))

@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    if request.method == 'POST':
        titulo = request.form['titulo-tarefa']
        data = request.form['data-conclusao']
        Tarefa(titulo, data).salvar_tarefa()
        return redirect(url_for('agenda'))
    
    tarefas = Tarefa.obter_tarefas()
    return render_template('agenda.html', titulo='Minha Agenda', tarefas=tarefas)

@app.route('/toggle/<int:idTarefa>', methods=['POST'])
def toggle(idTarefa):
    tarefa = Tarefa.id(idTarefa)
    if tarefa:
        novo_estado, data_hora = tarefa.alternar_conclusao()
        return jsonify({"concluida": novo_estado, "data_hora": data_hora})
    return jsonify({"erro": "Nao encontrado"}), 404

@app.route('/delete/<int:idTarefa>')
def delete(idTarefa):
    tarefa = Tarefa.id(idTarefa)
    if tarefa and tarefa.excluir_tarefa():
        return redirect(url_for('agenda'))
    return redirect(url_for('agenda'))

@app.route('/update/<int:idTarefa>', methods=['GET', 'POST'])
def update(idTarefa):
    if request.method == 'POST':
        titulo = request.form['titulo-tarefa']
        data = request.form['data-conclusao']
        Tarefa(titulo, data, idTarefa).atualizar_tarefa()
        return redirect(url_for('agenda'))
    
    tarefas = Tarefa.obter_tarefas()
    selecionada = Tarefa.id(idTarefa)
    return render_template('agenda.html', titulo='Editando Tarefa', tarefas=tarefas, tarefa_selecionada=selecionada)

