from flask import Flask, request, jsonify
from bson import json_util

from data import *

@app.route('/')
def home():
    return 'API ON'

@app.route('/api/usuario',methods=['POST','GET'])
def api_usuario():
    data=request.get_json()
    if valida_usuario(data['Email'],data['Senha'],db):
        retorno=busca_alarme(data['Email'],db)
        retorno = json.loads(json_util.dumps(retorno)) 
    else:
        retorno={'Status':'Usuario não encontrado'}
    return jsonify(retorno[0])

@app.route('/api/cadastro_usuario',methods=['POST','GET'])
def cadastro_usuario():
    data=request.get_json()
    if novo_usuario(data['Email'],data['Nome'],data['Senha'],db):
        cria_alarme(data['Email'],db)
        retorno={'Usuario':True}
    else:
        retorno={'Usuario':False}
    return jsonify(retorno)

@app.route('/api/cria_usuario',methods=['POST'])
def api_cria_alarme():
    data=request.get_json()
    email=data['Email']
    nome=data['Nome']
    senha=data['Senha']
    if (novo_usuario(email,nome,senha,db) and cria_alarme(email,db)):
        return True
    return False

@app.route('/api/statusalarme/<id>')
def api_alarme(id):
    retorno=alarme(id,db)
    return jsonify(retorno)

@app.route('/api/presenca',methods=['POST','GET'])
def recebe_api():
    data=request.get_json()
    return jsonify(atualiza_alarme(data['Email'],data['status'],data['estado_sensor'],data['estado_buzzer'],db))