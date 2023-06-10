from flask import Flask, request, jsonify, render_template,redirect,session,url_for
from flask_session import Session
apiUrl = 'http://172.17.0.3:5000/api/presenca'
url_get = 'http://172.17.0.3:5000/api/usuario'
url_cadastro = 'http://172.17.0.3:5000/api/cadastro_usuario'

from app import app
from helpers import *

@app.route('/')
def index():
    #render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if not session.get('usuario'):
        return render_template('login.html')
    return redirect(url_for('alarme'))

@app.post('/login')
def autenticar():
    usuario=envia_usuario(request.form['email'],request.form['senha'],url_get)
    if usuario['Status']!='Usuario não encontrado':
        session['usuario']=str(request.form.get('email'))
        session['senha']=str(request.form.get('senha'))
        return redirect(url_for('alarme'))
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/alarme')
def alarme():
    if not session.get('usuario'):
        return redirect(url_for('login'))
    alarme=envia_usuario(session.get('usuario'),session.get('senha'),url_get)
    return render_template('alarme.html',alarme=alarme,titulo='Alarme')

@app.post('/status_alarme/<id>')
def status_alarme(id):
    if atualiza_alarme(id,request.form.get('status'),sensor='Ativado',buzzer='Ativado'):
        return redirect(url_for('alarme'))
    return redirect(url_for('alarme'))

@app.route('/cadastrar_usuario')
def cadastrar_usuario():
    return render_template('cadastro_usuario.html',titulo='Cadastro de Usuario')

@app.post('/cadastrar_usuario')
def cadastrar_api():
    retorno=cadastra_usuario_api(request.form['email'],request.form['nome'],request.form['senha'],url_cadastro)
    if retorno['Usuario']:
        session['usuario']=str(request.form.get('email'))
        session['senha']=str(request.form.get('senha'))
        return redirect(url_for('alarme'))
    else:
        return render_template('cadastro_usuario.html',titulo='Cadastro de Usuario',erro='Erro no Cadastro')