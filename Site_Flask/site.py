from flask import Flask, request, jsonify, render_template,redirect,session,url_for
from flask_session import Session
import requests
import toml
with open('config.toml', 'r') as file:
    config = toml.load(file)
apiUrl = config['API_PADRAO']
url_get = config['API_GET_STATUS']
url_alarme = config['API_ALARME']

def envia_usuario(email,senha,url):
    json={'Email':email,'Senha':senha}
    response = requests.get(url, json=json)
    response.raise_for_status()
    return response.json()

def atualiza_alarme(id,status,sensor,buzzer,url):
    json={'Email':id,'status':status,'estado_sensor':sensor,'estado_buzzer':buzzer}
    response = requests.post(url, json=json)
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

@app.route('/alarme')
def alarme():
    alarme=envia_usuario(session.get('usuario'),session.get('senha'),url_get)
    return render_template('alarme.html',alarme=alarme)

@app.post('/status_alarme/<id>')
def status_alarme(id):
    if atualiza_alarme(id,request.form.get('status'),'Ativado','Ativado',apiUrl):
        return redirect(url_for('alarme'))
    return redirect(url_for('alarme'))

@app.route('/cadastrar_usuario')
def cadastrar_usuario():
    pass

app.run(port=8085, host='0.0.0.0',debug=True)