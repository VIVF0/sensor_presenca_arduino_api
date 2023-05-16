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

db=MongoClient('')

def criptografar(senha):
    hash_senha=sha256(senha.encode())
    return hash_senha.digest()

def novo_usuario(email,nome,senha):
    try:
        db.usuario.insert_one(
            {
                'Email':email,
                'Nome':nome,
                'Senha':criptografar(senha)
            }
        )
        return True
    except:
        return False
    
def cria_alarme(email):
    try:
        return db.usuario.insert_one(
            {
                'Email':email,
                'Sensor':'Desligado',
                'Buzzer':'Desligado',
                'Status':'Desligado'
            }
        )
    except:
        return False
    
def atualiza_alarme(id,estado_sensor,estado_buzzer,estado_status):
    try:
        db.usuario.update_one(
            {
                '_id':ObjectId(id)
            },
            {'$set':
                {
                    'Sensor':estado_sensor,
                    'Buzzer':estado_buzzer,
                    'Status':estado_status,
                }
            }
        )
        return True
    except:
        return False
    
def valida_usuario(email,senha):
    try:
        resultado=db.usuario.fin({'Email':email,'Senha':criptografar(senha)})
        if resultado!=None:
            return True
        return False
    except:
        return False

def busca_alarme(email):
    resultado=db.alarme.fin({'Email':email})
    if resultado!=None:
        return resultado
    
def alarme(id):
    resultado=db.alarme.fin({'_id':id})
    if resultado!=None:
        return resultado


app=Flask(__name__)
app.secrety_key='api_arduino'

@app.route('/')
def home():
    return 'API ON'

@app.route('/api/usuario',methods=['POST'])
def api_usuario():
    data=request.get_json()
    if valida_usuario(data['Email'],data['Senha']):
        alarme=busca_alarme(data['Email'])
        retorno=alarme['Status']
    else:
        retorno={'Status':'Usuario não encontrado'}
    return jsonify(retorno)

@app.rout('/api/criaalarme',methods=['POST'])
def api_cria_alarme():
    data=request.get_json()
    identifica=cria_alarme(data['Email'])
    retorno={'_id':identifica.inserted_id}
    return jsonify(retorno)

'''@app.route('/api/statusalarme/<id>')
def api_alarme(id):
    #consulta o banco para ver o estado do alarme definido pelo usuario
    retorno=alarme(id)
    return jsonify(retorno)'''

@app.route('/api/post/presenca',methods=['POST'])
def recebe_api():
    #recebe um aviso que o sensor pegou um presença e a nova distancia
    data=request.get_json()
    if atualiza_alarme(data['email'],data['estado_sensor'],data['estado_buzzer']):
        return 'True'
    return 'False'

app.run(host='0.0.0.0')