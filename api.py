'''
    Projeto:
    Alarme feito no esp32 usando buzzer e sonar, criacao de usuario pelo celular
    em uma webpage, e logar por uma webpage hospedada pelo esp32,
    o sensor quando ativado pelo usuario fica verificando a presenca pela passagem pelo sonar
    quando detecta a passagem de alguem, faz um post para a api e ativa o buzzer,
    a api pega o post da placa e atualiza a colecao alarme o sensor como ativo e buzzer como ativo
    (nisso o status esta como ativado pelo usuario ter ativado o a deteccao)
    o usuario pode desligar por uma webpage, podendo desligar o sensor, o buzzer ou a deteccao
'''

from flask import Flask, request, jsonify
from pymongo import MongoClient
from hashlib import sha256
from bson import ObjectId
import json

cliente=MongoClient('mongodb://172.17.0.2:27017')
db=cliente.Sensor

def criptografar(senha):
    hash_senha=sha256(senha.encode())
    return hash_senha.digest()

def novo_usuario(email,nome,senha,db):
    try:
        banco=db['usuario']
        return banco.insert_one(
            {
                'Email':email,
                    'Nome':nome,
                    'Senha':criptografar(senha)
                }
        )
        return True
    except:
        return False
    
def cria_alarme(email,db):
    try:
        banco=db['alarme']
        return banco.insert_one(
            {
                'Email':email,
                'Sensor':'Desligado',
                'Buzzer':'Desligado',
                'Status':'Desligado'
            }
        )
    except:
        return False
    
def atualiza_alarme(Email,estado_status,estado_sensor,estado_buzzer,db):
    try:
        banco=db['alarme']
        banco.update_one(
            {
                'Email':Email
            },
            {'$set':
                {
                    'Sensor':estado_sensor,
                    'Buzzer':estado_buzzer,
                    'Status':estado_status,
                }
            }
        )
        print('Foi')
        return True
    except:
        return False
    
def valida_usuario(email,senha,db):
    try:
        banco=db['usuario']
        resultado=banco.find({'Email':email,'Senha':criptografar(senha)})
        if resultado!=None:
            return True
        return False
    except:
        return False

def busca_alarme(email, db):
    banco = db['alarme']
    resultado = banco.find({'Email': email})
    if resultado is not None:
        return list(resultado)  
    return []

def alarme(id, db):
    banco = db['alarme']
    resultado = banco.find({'_id': id})
    if resultado is not None:
        return list(resultado)  
    return []


app=Flask(__name__)
app.secrety_key='api_arduino'

@app.route('/')
def home():
    return 'API ON'

from bson import json_util

@app.route('/api/usuario',methods=['POST','GET'])
def api_usuario():
    data=request.get_json()
    if valida_usuario(data['Email'],data['Senha'],db):
        retorno=busca_alarme(data['Email'],db)
        retorno = json.loads(json_util.dumps(retorno)) 
    else:
        retorno={'Status':'Usuario não encontrado'}
    return jsonify(retorno[0])

@app.route('/api/criaalarme',methods=['POST'])
def api_cria_alarme():
    data=request.get_json()
    identifica=cria_alarme(data['Email'],db)
    retorno={'_id':identifica.inserted_id}
    return jsonify(retorno)

@app.route('/api/statusalarme/<id>')
def api_alarme(id):
    #consulta o banco para ver o estado do alarme definido pelo usuario
    retorno=alarme(id,db)
    return jsonify(retorno)

@app.route('/api/presenca',methods=['POST','GET'])
def recebe_api():
    #recebe um aviso que o sensor pegou um presença e a nova distancia
    data=request.get_json()
    return jsonify(atualiza_alarme(data['Email'],data['status'],data['estado_sensor'],data['estado_buzzer'],db))

app.run(debug=True)
