from flask import Flask, request, jsonify, render_template,redirect,session,url_for
from flask_session import Session
import requests

apiUrl = 'http://172.17.0.3:5000/api/presenca'
url_get = 'http://172.17.0.3:5000/api/usuario'
url_cadastro = 'http://172.17.0.3:5000/api/cadastro_usuario'

def envia_usuario(email,senha,url):
    json={'Email':email,'Senha':senha}
    response = requests.get(url, json=json)
    response.raise_for_status()
    return response.json()

def cadastra_usuario_api(email,nome,senha,url):
    json={'Email':email,'Senha':senha,'Nome':nome}
    response = requests.get(url, json=json)
    response.raise_for_status()
    return response.json()

def atualiza_alarme(id,status='Ativado',sensor='Ativado',buzzer='Ativado'):
    global apiUrl
    json={'Email':id,'status':status,'estado_sensor':sensor,'estado_buzzer':buzzer}
    response = requests.post(apiUrl, json=json)
    response.raise_for_status()
    return response.json()

app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

app.run(port=8085, host='0.0.0.0',debug=True)